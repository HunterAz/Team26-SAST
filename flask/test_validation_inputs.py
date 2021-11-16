import pytest
from website.controller import securityController as SC
from website.controller.passwordController import PasswordController as PC

#Testing for valid number inputs#
@pytest.fixture()
def input_num_valid():
    result = SC.validate_number("1")
    return result

@pytest.fixture()
def input_num_invalid():
    result = SC.validate_number("ad12")
    return result

def test_inputnum_valid(input_num_valid):
    assert input_num_valid == True

def test_inputnum_invalid(input_num_invalid):
    assert input_num_invalid == None

#Testing for valid text inputs#
@pytest.fixture()
def input_text_valid():
    result = SC.validate_text("dasdad123!")
    return result

@pytest.fixture()
def input_text_invalid():
    result = SC.validate_text("~dasd~")
    return result

def test_inputtext_valid(input_text_valid):
    assert input_text_valid == input_text_valid

def test_inputtext_invalid(input_text_invalid):
    assert input_text_invalid == None


#Testing for valid email inputs#
@pytest.fixture()
def input_email_valid():
    result = SC.validate_email("test@gmail.com")
    return result

@pytest.fixture()
def input_email_invalid():
    result = SC.validate_email("dasd@testing.coms")
    return result

def test_inputemail_valid(input_email_valid):
    assert input_email_valid == input_email_valid

def test_inputemail_invalid(input_email_invalid):
    assert input_email_invalid == None

#Testing for valid symbol inputs#
@pytest.fixture()
def input_symbol_valid():
    result = SC.validate_allow_symbols("~test!", "~!")
    return result

@pytest.fixture()
def input_symbol_invalid():
    result = SC.validate_allow_symbols("-test!", "~!")
    return result

def test_inputsym_valid(input_symbol_valid):
    assert input_symbol_valid == input_symbol_valid

def test_inputsym_invalid(input_symbol_invalid):
    assert input_symbol_invalid == None

#Testing for valid email inputs#
@pytest.fixture()
def input_date_valid():
    result = SC.validate_date("2021-10-10")
    return result

@pytest.fixture()
def input_date_valid():
    result = SC.validate_date("19999-123-10")
    return result

def test_inputdate_valid(input_date_valid):
    assert input_date_valid == input_date_valid

def test_inputdate_invalid(input_date_valid):
    assert input_date_valid == None



#Testing for password
@pytest.fixture()
def input_pw_valid():
    result = PC.verify_hash("testuser","testuser","$pbkdf2-sha256$29000$0prTmlNq7X0PYWyNEeK8Vw$iLrk67xr8ijAebEsRFqEomRYYsTY4RKIVfGbCkmXGAQ")
    return result

@pytest.fixture()
def input_pw_invalid():
    result = PC.verify_hash("tetuser123","tetuser123", "$pbkdf2-sha256$29000$0prTmlNq7X0PYWyNEeK8Vw$iLrk67xr8ijAebEsRFqEomRYYsTY4RKIVfGbCkmXGAQ")
    return result

def test_inputpw_valid(input_pw_valid):
    assert input_pw_valid == True

def test_inputpw_invalid(input_pw_invalid):
    assert input_pw_invalid == False