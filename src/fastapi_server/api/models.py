from fastapi import APIRouter, UploadFile, Depends, HTTPException, status
from fastapi.responses import StreamingResponse, FileResponse
from src.fastapi_server.services.users import get_current_user_id
from src.fastapi_server.services.files import FilesService
from src.fastapi_server.services.models import ModelsService

router = APIRouter(
    prefix='/models',
    tags=['models'],
)


@router.post('/preprocessing', name='Preprocessing')
def model_preprocessing(file: UploadFile, files_service: FilesService = Depends(),
                        user_id: int = Depends(get_current_user_id), model: ModelsService = Depends()):
    """
    Предобработка данных
    """
    data = files_service.upload(file.file)
    files_service.save_file(data, model.data_file)
    data_preprocessing = model.preprocessing(data, user_id)
    files_service.save_file(data_preprocessing, model.data_preproc_file)
    report = files_service.download(data_preprocessing)
    return StreamingResponse(report, media_type='text/csv',
                             headers={'Content-Disposition': 'attachment; filename=data_preprocessing.csv'})


@router.post('/fit', name='Fit model')
def model_fit(file: UploadFile, files_service: FilesService = Depends(),
              user_id: int = Depends(get_current_user_id), model: ModelsService = Depends()):
    """
    Обучение модели
    """
    data = files_service.upload(file.file)
    data_to_predict = model.fit(data, user_id)
    files_service.save_file(data_to_predict, model.data_test_file)
    return True


@router.post('/predict', name='Model predict')
def model_predict(file: UploadFile, files_service: FilesService = Depends(),
                  user_id: int = Depends(get_current_user_id), model: ModelsService = Depends()):
    """
    Предсказание модели
    """
    data = files_service.upload(file.file)
    data_predict = model.predict(data, user_id)
    files_service.save_file(data_predict, model.data_predict_file)
    files_service.save_file(model.predict_all(), model.data_all_predict_file)
    report = files_service.download(data_predict)
    return StreamingResponse(report, media_type='text/csv',
                             headers={'Content-Disposition': 'attachment; filename=data_predict.csv'})


@router.get('/download/{type_id}', name='Download data')
def download(type_id: int, user_id: int = Depends(get_current_user_id),
             model: ModelsService = Depends()):
    """
    Скачивание данных для dash'а.
    type_id:
    1 - исходный файл;
    2 - предобработанный файл;
    3 - файл с предсказаниями;
    4 - модель
    5 - исходный файл с предсказаниями
    """
    if type_id not in (1, 2, 3, 4, 5):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такого файла нет')
    path = model.download(type_id, user_id)

    return FileResponse(path=path, filename='data.csv', media_type='text/csv')
