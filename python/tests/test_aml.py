from uuid import UUID
from dataspike import Api, AMLEntity, AMLResponse, AMLSearchRequest, SourceData, DataSource
from conftest import to_json

from pydantic_factories import ModelFactory


class AMLEntityFactory(ModelFactory):
    __model__ = AMLEntity
    __allow_none_optionals__ = False


class AMLResponseFactory(ModelFactory):
    __model__ = AMLResponse
    __allow_none_optionals__ = False


class AMLRequestFactory(ModelFactory):
    __model__ = AMLSearchRequest
    __allow_none_optionals__ = False


async def test_aml_get(aioresponses, api: Api):
    search_id = UUID(int=21314351524642462451465345)

    aml = AMLEntityFactory.build()
    aioresponses.get(f"https://api.dataspike.io/api/v3/aml/search/{search_id}", body=to_json(aml))

    got = await api.aml.get(search_id)
    aioresponses.assert_called_once()
    assert got == aml


async def test_aml_search(aioresponses, api: Api):
    request = AMLRequestFactory.build()
    response = AMLResponseFactory.build()
    aioresponses.post("https://api.dataspike.io/api/v3/aml/search", body=to_json(response))

    got = await api.aml.search(request)
    aioresponses.assert_called_once()
    assert got == response


async def test_aml_unknown_data_source(aioresponses, api: Api):
    search_id = UUID(int=21314351524642462451465345)

    aml: AMLEntity = AMLEntityFactory.build()
    aml.fields.sources = [SourceData(source_id="XYZ_QWERTY_NEW", name="new")]
    aioresponses.get(f"https://api.dataspike.io/api/v3/aml/search/{search_id}", body=to_json(aml))
    got = await api.aml.get(search_id)
    aioresponses.assert_called_once()
    assert got == aml
    assert got.fields.sources and len(got.fields.sources) == 1
    assert got.fields.sources[0].source_id == "XYZ_QWERTY_NEW"


async def test_aml_known_data_source(aioresponses, api: Api):
    search_id = UUID(int=21314351524642462451465345)

    aml: AMLEntity = AMLEntityFactory.build()
    aml.fields.sources = [SourceData(source_id=DataSource.EUMOSTWANTED, name="known")]
    aioresponses.get(f"https://api.dataspike.io/api/v3/aml/search/{search_id}", body=to_json(aml))
    got = await api.aml.get(search_id)
    aioresponses.assert_called_once()
    assert got == aml
    assert got.fields.sources and len(got.fields.sources) == 1
    assert isinstance(got.fields.sources[0].source_id, DataSource)
