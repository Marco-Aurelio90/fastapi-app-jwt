import fastapi
import fastapi.security as security
import sqlalchemy.orm as orm
import schemas as schemas
import services as services

app = fastapi.FastAPI()


@app.post("/api/v1/users")
async def register_user(
        user: schemas.UserRequest, db: orm.Session = fastapi.Depends(services.get_db)
):
    # call to check if user with email exist
    db_user = await services.getUserByEmail(email=user.email, db=db)
    # if user found throw exception(it means the same user 2times)
    if db_user:
        raise fastapi.HTTPException(status_code=400, detail="Email already exist, try another one")

    # create the user and return a token
    db_user = await services.create_user(user=user, db=db)
    return await services.create_token(db_user)


@app.post("/api/v1/login")
async def login_user(
        form_data: security.OAuth2PasswordRequestForm = fastapi.Depends(),
        db: orm.Session = fastapi.Depends(services.get_db)
):
    db_user = await services.login(email=form_data.username, password=form_data.password, db=db)

    # Invalid login throw exception
    if not db_user:
        raise fastapi.HTTPException(status_code=401, detail="Wrong Login Credentials!")

    # Create and return the token
    return await services.create_token(db_user)


@app.get("/api/users/current-user", response_model=schemas.UserResponse)
async def current_user(user: schemas.UserResponse = fastapi.Depends(services.current_user)):
    return user
