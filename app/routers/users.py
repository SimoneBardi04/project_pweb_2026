from fastapi import APIRouter, Path, HTTPException, Query
from app.models.userDB import User, UserCreate
from app.models.registration import Registration
from app.data.db import SessionDep
from typing import Annotated
from sqlmodel import select, delete

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/")
def get_all_user(
    session: SessionDep,
    sort: Annotated[bool, Query(description="Ordinami gli utenti in ordine crescente o decrescente")]=False
    )->list[User]:
    # Restituisce la lista di tutti gli utenti

    users = session.exec(select(User))

    if sort:
        return sorted(users, key=lambda x: x.username)
    else:
        return list(users)

@router.get("/{username}")
def get_user_by_username(
    session: SessionDep,
    username: Annotated[str, Path(description="Username dell'utente")]
    )->User:
    #Restituisce l'utente con l'username cercato

    user=session.get(User, username)

    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="Utente non trovato")
    
@router.post("/")
def new_user(
    session:SessionDep,
    user:UserCreate):
    
    #Aggiungi un nuovo utente
    
    userExist=session.get(User, user.username)
    
    if userExist:
        raise HTTPException(status_code=409, detail="L'Username esiste già non trovato")
        #TODO: Controllare meglio l'errore come viene mostrato, possibile fix?
    else:
        newUser = User.model_validate(user)
        session.add(newUser)
        session.commit()
        return "Utente aggiunto con successo"
    
@router.delete("/")
def delete_users(
    session: SessionDep
):
    session.exec(delete(User))
    session.commit()
    return "Tutti gli utenti sono stati eliminati"

@router.delete("/{username}")
def delete_user(
    session: SessionDep,
    username: Annotated[str, Path(description="Username dell'utente")]
):
    user=session.get(User, username)

    if not user:
        raise HTTPException(status_code=404, detail="Utente non trovato")
    
    registrazioni = session.exec(select(Registration).where(Registration.username==username)).all()

    for i in registrazioni:
        session.delete(i)

    session.delete(user)
    session.commit()

    return "Utente rimosso"
    
