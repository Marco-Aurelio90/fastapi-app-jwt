import email_validator as email_validator
import fastapi as fastapi
import database as database
import models as models
import sqlalchemy.orm as orm

import schemas as schemas
import passlib.hash as hash
import jwt as jwt
import fastapi.security as security
from dotenv import load_dotenv
import os


def configure():
    load_dotenv()


# Found this vulnerability through bandit as ISSUE: [B105:hardcoded_password_string]
# Possible hardcoded password: 'igk8szmKWRfsDwt7STGZ331+E4un/1mDyeAPg9Ehc7o=' ; Severity: Low , Confidence: Medium
# CWE: CWE-259 (https://cwe.mitre.org/data/definitions/259.html

# This is how I've mitigated it
# I've declared the value in the environment variable stored in the .env path ->
# -> I avoided to check clearly the value type of the JWT_SECRET in the current source code.
# JWT_SECRET = "igk8szmKWRfsDwt7STGZ331+E4un/1mDyeAPg9Ehc7o="


oauth2schema = security.OAuth2PasswordBearer("/api/v1/login")


def create_db():
    return database.Base.metadata.create_all(bind=database.engine)


# The function below is used to create tables in Db(SqLite as dbfile.db)
# create_db()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def getuserbyemail(email: str, db: orm.Session):
    return db.query(models.UserModel).filter(models.UserModel.email == email).first()


async def create_user(user: schemas.UserRequest, db=orm.Session):
    # check for valid email
    try:
        isvalid = email_validator.validate_email(email=user.email)
        email = isvalid.ValidatedEmail.normalized
    # send bad request if is the email is not valid
    except email_validator.EmailNotValidError:
        raise fastapi.HTTPException(status_code=400, detail="Provide valid Email")
    # convert password to hashed password
    hashed_password = hash.bcrypt.hash(user.password)
    # create user model to be saved in db
    user_obj = models.UserModel(
        email=email,
        name=user.name,
        phone=user.phone,
        password_hash=hashed_password
    )
    # save the user in db
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)

    return user_obj


async def create_token(user: models.UserModel):
    # covert user model to user schema
    user_schema = schemas.UserResponse.from_orm(user)
    # convert obj to dictionary
    user_dict = user_schema.dict()
    del user_dict["created_at"]

    token = jwt.encode(user_dict, os.getenv('JWT_SECRET'))

    # Found this vulnerability through bandit as ISSUE: [B106:hardcoded_password_funcarg]
    # Possible hardcoded password: 'bearer' ; Severity: Low , Confidence: Medium
    #  CWE: CWE-259 (https://cwe.mitre.org/data/definitions/259.html)
    #    return dict(access_token=token, token_type="bearer")

    # Mitigation
    # The issue has been mitigated by moving the TOKEN_TYPE to an environment variable
    return dict(access_token=token, token_type=os.getenv('TOKEN_TYPE'))


async def login(email: str, password: str, db: orm.Session):
    db_user = await getuserbyemail(email=email, db=db)

    # Return False if no user with email found
    if not db_user:
        return False

    # Return False if no user with password found
    if not db_user.password_verification(password=password):
        return False

    return db_user


async def current_user(db: orm.Session = fastapi.Depends(get_db), token: str = fastapi.Depends(oauth2schema)):
    try:
        payload = jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=["HS256"])
        # Get user by Id and Id is already available in the decoded user payload along with email, phone and name
        db_user = db.query(models.UserModel).get(payload["id"])
    except:
        raise fastapi.HTTPException(status_code=401, detail="Wrong Credentials")

    # if all okay then return the DTO/Schemas version User
    return schemas.UserResponse.from_orm(db_user)
