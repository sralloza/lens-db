import json
from unittest import mock

import pytest

from lens_db.src.config import CREDENTIALS_PATH
from lens_db.src.credentials import Credentials, get_credentials, save_credentials
from lens_db.src.exceptions import NoCredentialsError

encryption_data_test = (
    ("hello this is a test", "uryyb guvf vf n grfg"),
    ("used rot thirteen", "hfrq ebg guvegrra"),
    ("hello world", "uryyb jbeyq"),
)


class TestCredentials:
    def test_attributes(self):
        creds = Credentials("a", "b")
        assert hasattr(creds, "enc_user")
        assert hasattr(creds, "enc_pass")

    @mock.patch("lens_db.src.credentials.Credentials._encrypt")
    def test_from_unencrypted(self, encrypt_mock):
        encrypt_mock.side_effect = lambda x: "enc-%s" % x
        creds = Credentials.from_unencrypted("-user-", "-pass-")

        assert creds.enc_user == "enc--user-"
        assert creds.enc_pass == "enc--pass-"

        encrypt_mock.assert_any_call("-user-")
        encrypt_mock.assert_any_call("-pass-")
        assert encrypt_mock.call_count == 2

    @mock.patch("lens_db.src.credentials.CREDENTIALS_PATH")
    def test_load_from_file(self, creds_path_mock):
        data = json.dumps({"enc_user": "--user--", "enc_pass": "--pass--"})
        creds_path_mock.read_text.return_value = data
        creds = Credentials.load_from_file()
        assert creds.enc_user == "--user--"
        assert creds.enc_pass == "--pass--"

    @mock.patch("lens_db.src.credentials.Credentials._decrypt")
    def test_decrypt(self, decrypt_mock):
        decrypt_mock.side_effect = lambda x: "dec-%s" % x
        creds = Credentials("enc_username", "enc_password")
        uncreds = creds.decrypt()

        assert hasattr(uncreds, "username")
        assert hasattr(uncreds, "password")
        assert uncreds.username == "dec-enc_username"
        assert uncreds.password == "dec-enc_password"

        decrypt_mock.assert_any_call("enc_username")
        decrypt_mock.assert_any_call("enc_password")
        assert decrypt_mock.call_count == 2

    @pytest.mark.parametrize("normal, encrypted", encryption_data_test)
    def test__decrypt(self, normal, encrypted):
        assert Credentials._decrypt(encrypted) == normal

    @pytest.mark.parametrize("normal, encrypted", encryption_data_test)
    def test__encrypt(self, normal, encrypted):
        assert Credentials._encrypt(normal) == encrypted

    @mock.patch("lens_db.src.credentials.CREDENTIALS_PATH")
    def test_save(self, creds_path_mock):
        data = {"enc_user": "--user--", "enc_pass": "--pass--"}
        string_data = json.dumps(data)
        creds = Credentials(**data)
        creds.save()

        creds_path_mock.parent.mkdir.assert_called_once_with(
            exist_ok=True, parents=True
        )
        creds_path_mock.write_text.assert_called_with(string_data)


@pytest.mark.parametrize("exist", [True, False])
@mock.patch("lens_db.src.credentials.Credentials")
@mock.patch("lens_db.src.credentials.CREDENTIALS_PATH")
def test_get_credentials(creds_path_mock, creds_mock, exist):
    creds_path_mock.exists.return_value = exist

    if not exist:
        with pytest.raises(NoCredentialsError):
            get_credentials()
        return

    creds = get_credentials()

    assert creds == creds_mock.load_from_file.return_value.decrypt.return_value
    creds_mock.load_from_file.assert_called_once_with()
    creds_mock.load_from_file.return_value.decrypt.assert_called_once_with()


@mock.patch("lens_db.src.credentials.Credentials.from_unencrypted")
def test_save_credentials(creds_fu_mock):
    creds = save_credentials("-user-", "-pass-")

    creds_fu_mock.assert_called_once_with("-user-", "-pass-")
    creds_fu_mock.return_value.save.assert_called_once_with()
    assert creds == creds_fu_mock.return_value.save.return_value
