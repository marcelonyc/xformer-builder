import filestoreprovider.apiprovider as APIProvider
import filestoreprovider.gdriveprovider as GDriveProvider
import filestoreprovider.localfsprovider as LocalFSProvider
import filestoreprovider.s3provider as S3Provider

__all__ = {
    "apiprovider": APIProvider,
    "gdriveprovider": GDriveProvider,
    "localfs": LocalFSProvider,
    "s3provider": S3Provider,
}
