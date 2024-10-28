""" unit/integration tests of the oaio client package. """
import os
import shutil

import pytest

from conftest import skip_gitlab_ci

from ae.base import (
    TESTS_FOLDER, load_dotenvs, os_path_abspath, os_path_isdir, os_path_isfile, os_path_join, write_file)
from ae.oaio_model import CREATE_WRITE_ACCESS, FILES_VALUES_KEY, OaiObject, ROOT_VALUES_KEY, now_stamp
from ae.paths import normalize

from ae.oaio_client import OaioClient


load_dotenvs()


@pytest.fixture
def my_server():
    """ on local machine connect to personal server in order to do integration tests """
    ocl = OaioClient(os.environ['OAIO_HOST_NAME'],
                     {'username': os.environ['OAIO_USERNAME'], 'password': os.environ['OAIO_PASSWORD']},
                     )
    yield ocl


def _csh_file_content(client_obj: OaioClient, oai_obj: OaiObject) -> bytes:
    """ download file content from cloud storage host """
    # noinspection PyProtectedMember
    files, csh_api, client_path, server_path = client_obj._object_client_server_file_paths(oai_obj, upload=True)
    assert csh_api
    assert len(files) == 1

    return csh_api.deployed_file_content(os_path_join(server_path, files[0]))


def _csh_file_remove(client_obj: OaioClient, oai_obj: OaiObject) -> str:
    """ delete file content from cloud storage host """
    # noinspection PyProtectedMember
    files, csh_api, client_path, server_path = client_obj._object_client_server_file_paths(oai_obj, upload=True)
    assert csh_api
    assert len(files) == 1

    err_msg = csh_api.delete_file_or_folder(os_path_join(server_path, files[0]))
    return err_msg


class TestInstantiation:
    def test_args(self):
        cre_args = {'cre_key': 'cre_val'}
        loc_oz = {}
        loc_path = 'local/root/path'

        ocl = OaioClient("hOsT", cre_args, 'app_id', 'dev_id', 'csh_id', loc_oz, loc_path, 369.12)

        assert "hOsT" in ocl.base_url
        assert ocl.credentials == cre_args
        assert ocl.app_id == 'app_id'
        assert ocl.device_id == 'dev_id'
        assert ocl.csh_default_id == 'csh_id'
        assert ocl.local_objectz is loc_oz
        assert ocl.local_root_path == os_path_abspath(loc_path)
        assert ocl.auto_sync_seconds == 369.12

    def test_defaults(self):
        ocl = OaioClient("", {})

        assert ocl.app_id
        assert ocl.device_id
        assert ocl.csh_default_id == 'Digi'
        assert ocl.local_root_path == normalize("{ado}/oaio_root/")

    def test_invalid_host_instantiation_args(self):
        ocl = OaioClient("", {})

        assert ocl
        assert not ocl.synchronize_with_server_if_online()


@skip_gitlab_ci
class TestMyServer:
    def test_connect(self, my_server):
        assert my_server.error_message == ""
        assert my_server.connected

    def test_register_file(self, my_server):
        assert my_server.error_message == ""
        oai_obj = None
        stamp = now_stamp()
        dir_path = os_path_abspath(os_path_join(TESTS_FOLDER, 'tst_fil_dir'))
        fil_path = os_path_join(dir_path, 'tst_fil.tst')
        fil_content = b"test file \x00 binary content \x01\x02\x03\xff"
        local_object_count = len(my_server.local_objectz)
        try:
            os.makedirs(dir_path)
            write_file(fil_path, fil_content)

            oai_obj = my_server.register_file(fil_path, stamp=stamp)
            assert my_server.error_message == ""
            assert oai_obj is not None

            assert oai_obj.oaio_id
            assert oai_obj.csh_id
            assert ROOT_VALUES_KEY not in oai_obj.client_values
            assert FILES_VALUES_KEY in oai_obj.client_values
            assert len(oai_obj.client_values[FILES_VALUES_KEY]) == 1
            assert normalize(oai_obj.client_values[FILES_VALUES_KEY][0]) == fil_path
            assert not oai_obj.server_values
            assert oai_obj.client_stamp == stamp
            assert not oai_obj.server_stamp
            assert oai_obj.csh_write_access == CREATE_WRITE_ACCESS

            assert len(my_server.local_objectz) == local_object_count + 1
            assert oai_obj.oaio_id in my_server.local_objectz
            assert my_server.local_objectz[oai_obj.oaio_id] == oai_obj

            assert os_path_isfile(fil_path)
            assert _csh_file_content(my_server, oai_obj) == fil_content

        finally:
            if os_path_isdir(dir_path):
                shutil.rmtree(dir_path)
            if oai_obj:
                assert my_server.unregister_object(oai_obj.oaio_id)
                assert _csh_file_remove(my_server, oai_obj) == ""

    def test_register_folder_with_root(self, my_server):
        assert my_server.error_message == ""
        oai_obj = None
        stamp = now_stamp()
        root_path = os_path_abspath(os_path_join(TESTS_FOLDER, 'tst_fol_dir'))
        sub_dirs = ['sub_dir1', 'sub_dir3/sub_sub_dir']
        file_paths = ['tst_fil.tst',
                      os_path_join(sub_dirs[0], 'tst_sub1_fil.tst'),
                      os_path_join(sub_dirs[1], 'tst_sub3_sub_fil.tst'),
                      ]
        fil_content = b"test file \x00 binary content \x01\x02\x03\xff"
        local_object_count = len(my_server.local_objectz)
        csh_api = my_server._csh_api(my_server.csh_default_id)
        svr_path = ""
        try:
            for dir_nam in sub_dirs:
                os.makedirs(os_path_join(root_path, dir_nam))
            for fil_nam in file_paths:
                write_file(os_path_join(root_path, fil_nam), fil_content + fil_nam.encode())

            oai_obj = my_server.register_folder(root_path, stamp=stamp)

            assert my_server.error_message == ""
            assert oai_obj is not None

            assert oai_obj.oaio_id
            svr_path = os_path_join(oai_obj.oaio_id, stamp)
            assert oai_obj.csh_id
            assert ROOT_VALUES_KEY in oai_obj.client_values
            assert normalize(oai_obj.client_values[ROOT_VALUES_KEY]) == normalize(root_path)
            assert FILES_VALUES_KEY in oai_obj.client_values
            assert len(oai_obj.client_values[FILES_VALUES_KEY]) == len(file_paths)
            for fil_nam in file_paths:
                assert fil_nam in oai_obj.client_values[FILES_VALUES_KEY]
                assert os_path_isfile(normalize(os_path_join(root_path, fil_nam)))
                assert csh_api.deployed_file_content(os_path_join(svr_path, fil_nam)) == fil_content + fil_nam.encode()
            assert not oai_obj.server_values
            assert oai_obj.client_stamp == stamp
            assert not oai_obj.server_stamp
            assert oai_obj.csh_write_access == CREATE_WRITE_ACCESS

            assert len(my_server.local_objectz) == local_object_count + 1
            assert oai_obj.oaio_id in my_server.local_objectz
            assert my_server.local_objectz[oai_obj.oaio_id] == oai_obj

        finally:
            if os_path_isdir(root_path):
                shutil.rmtree(root_path)
            if oai_obj:
                assert my_server.unregister_object(oai_obj.oaio_id)
                if svr_path:
                    assert not csh_api.delete_file_or_folder(svr_path)

    def test_register_obj(self, my_server):
        assert my_server.error_message == ""
        oai_obj = None
        stamp = now_stamp()
        values = {'tst_str': 'tst_val', 'tst_int': 69}
        local_object_count = len(my_server.local_objectz)
        try:
            oai_obj = my_server.register_object(values, stamp=stamp)
            assert my_server.error_message == ""
            assert oai_obj is not None

            assert oai_obj.oaio_id
            assert oai_obj.csh_id
            assert oai_obj.client_values == values
            assert not oai_obj.server_values
            assert oai_obj.client_stamp == stamp
            assert not oai_obj.server_stamp
            assert oai_obj.csh_write_access == CREATE_WRITE_ACCESS

            assert len(my_server.local_objectz) == local_object_count + 1
            assert oai_obj.oaio_id in my_server.local_objectz
            assert my_server.local_objectz[oai_obj.oaio_id] == oai_obj

        except Exception as exc:
            assert False, f"re-raising test run exception: {exc}"

        finally:
            if oai_obj:
                assert my_server.unregister_object(oai_obj.oaio_id)
