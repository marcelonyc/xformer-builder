from database import database, xformer_store, users
from fastapi import HTTPException, status
from sqlalchemy import select, func, insert, update, and_ as _and
from sqlalchemy.exc import IntegrityError
from config.app_config import AppConfig
from lib.models import XformerData
from database import database, file_xformer_association, file_manager, users
import python_modules.code_validator.code_validator as code_validator
import base64
import os
import io
import sys
import logging

app_config = AppConfig()


def process_file_status(
    file_id: str,
    upload_id: str,
    file_size: int = 0,
    _user_id: str = None,
    msg: str = None,
):
    # Add upload to file manager
    insert_query = insert(file_manager).values(
        file_id=file_id,
        upload_id=upload_id,
        user_id=_user_id,
        file_size=file_size,
        last_update_message=msg,
    )
    update_query = (
        update(file_manager)
        .where(_and(file_id == file_id, upload_id == upload_id))
        .values(
            user_id=_user_id,
            file_size=file_manager.c.file_size + file_size,
            last_update_message=msg,
        )
    )
    try:
        database.execute_sync(insert_query)
    except IntegrityError as e:
        database.execute_sync(update_query)
    except Exception as e:
        logging.error("Could not write to database {e}".format(e=e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not write to database",
        )


def get_xformer_from_db(id: str, xformer_id: str) -> XformerData:

    select_query = (
        select(xformer_store)
        .join(users, xformer_store.c.user_id == users.c.id)
        .where(users.c.id == id)
        .where(xformer_store.c.id == xformer_id)
    )
    _xformer_from_db = database.fetch_all_sync(select_query)

    _xformer = XformerData(**_xformer_from_db[0])
    return _xformer


def process_file(file_id: str, upload_id: str, filename: str):

    filestoreprovider = app_config.filestoreprovider
    # Get user_id and xformer_id
    user_select = select(
        file_xformer_association.c.user_id,
        file_xformer_association.c.xformer_id,
    ).where(file_xformer_association.c.file_id == file_id)
    try:
        _user_id_result = database.fetch_all_sync(user_select)
    except Exception as e:
        process_file_status(
            file_id, upload_id, msg="Could not fetch user_id and xformer_id"
        )
        return
    if len(_user_id_result) == 0:
        msg = "User_id and xformer_id not found"
        process_file_status(file_id, upload_id, msg=msg)
        return

    _user_id = _user_id_result[0]["user_id"]
    _xformer_id = _user_id_result[0]["xformer_id"]

    _, file_extension = os.path.splitext(filename)
    _xformer = get_xformer_from_db(_user_id, _xformer_id)
    file_df = filestoreprovider.get_file(file_id, upload_id, file_extension)

    # Rename columns
    try:
        if _xformer.xformer.source_column != _xformer.xformer.target_column:
            # Add new columns
            for column in _xformer.xformer.target_column:
                if column not in file_df.columns:
                    file_df[column] = file_df[
                        _xformer.xformer.source_column[
                            _xformer.xformer.target_column.index(column)
                        ]
                    ]
    except Exception as e:
        process_file_status(file_id, upload_id, msg="Could not rename columns")
        return

    try:
        for _code in range(len(_xformer.xformer.code)):
            b64_code = _xformer.xformer.code[_code]

            if b64_code is not None and b64_code != "":
                field_name = _xformer.xformer.target_column[_code]
                _executable_code = base64.b64decode(b64_code).decode("utf-8")
                file_df[field_name] = file_df.apply(
                    lambda x: code_validator.safe_execute(
                        _executable_code, x[field_name], x
                    )["result"],
                    axis=1,
                )
    except Exception as e:
        process_file_status(file_id, upload_id, msg="Could not execute code")
        return

    stream = io.StringIO()
    try:
        stream.write(
            file_df[_xformer.xformer.target_column].to_csv(index=False)
        )
    except Exception as e:
        process_file_status(
            file_id, upload_id, msg="Could not save trasnformed file to memory"
        )
        return

    try:
        filestoreprovider.put_file(file_id, upload_id, stream)
        file_size = sys.getsizeof(stream.getvalue())
    except Exception as e:
        process_file_status(
            file_id, upload_id, msg="Could not save transformed file"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not write to filestore",
        )

    stream.close()

    process_file_status(
        file_id, upload_id, file_size, _user_id, msg="File processed"
    )


async def validate_file_id(file_id: str):

    file_exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Could not validate file ID",
    )

    select_query = select(file_xformer_association).where(
        file_xformer_association.c.file_id == file_id
    )

    try:
        _is_file_id = await database.fetch_all(select_query)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found",
        )
    if len(_is_file_id) == 0:
        raise file_exception
    else:
        return True


async def check_account_total_size(file_id: str):

    file_exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="File upload exceeds account limit",
    )

    select_query = select(func.sum(file_manager.c.file_size)).where(
        file_manager.c.user_id
        == select(file_xformer_association.c.user_id).where(
            file_xformer_association.c.file_id == file_id
        )
    )
    try:
        _storage_sum = await database.fetch_all(select_query)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found",
        )

    if (_storage_sum[0].get("sum_1") or 0) >= app_config.max_storage_size:
        raise file_exception

    return True
