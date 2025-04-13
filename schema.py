from strawberry.flask.views import GraphQLView
import strawberry
import datetime

from models import UserModel, MeetingModel
from db import Session



@strawberry.type
class Meeting:
    id: int
    title: str
    time: str
    content: str
    attendees: list["User"]


@strawberry.type
class User:
    id: int
    name: str
    email: str
    meetings: list["Meeting"]

@strawberry.type
class Query:
    @strawberry.field
    def get_user(self, id: int) -> User:
        # Get user by ID
        with Session() as session:
            user = session.get(UserModel, id)
            if user is None:
                raise ValueError(f"User with id={id} not found")

            return User(id = user.id, name = user.name, email= user.email, meetings = user.meetings)
    
    @strawberry.field
    def get_meeting(self, id: int) -> Meeting:
        # Get meeting by ID
        with Session() as session:
            meeting = session.get(MeetingModel, id)
            if meeting is None:
                raise ValueError(f"Meeting with id={id} not found")
            return Meeting(id = meeting.id, title=meeting.title, time=meeting.time, content=meeting.content, attendees = meeting.attendees)
    
    @strawberry.field
    def get_all_users(self) -> list[User]:
        # Get all users with their attendees
        with Session() as session:
            from sqlalchemy.orm import joinedload
            users = session.query(UserModel).options(joinedload(UserModel.meetings)).all()
            return [
                User(
                    id=user.id, 
                    name=user.name, 
                    email=user.email, 
                    meetings=[
                        Meeting(
                            id=meeting.id,
                            title=meeting.title,
                            time=str(meeting.time) if meeting.time else "",
                            content=meeting.content,
                            attendees=[]
                        ) for meeting in user.meetings
                    ]
                ) for user in users
            ]
    
    @strawberry.field
    def get_all_meetings(self) -> list[Meeting]:
        # Get all meetings with their attendees
        with Session() as session:
                from sqlalchemy.orm import joinedload
                meetings = session.query(MeetingModel).options(joinedload(MeetingModel.attendees)).all()
                return[
                    Meeting(
                        id=meeting.id,
                        title=meeting.title,
                        time=str(meeting.time) if meeting.time else "",
                        content=meeting.content,
                        attendees=[
                            User(
                                id=user.id, 
                                name=user.name, 
                                email=user.email,
                                meetings=[]
                            ) for user in meeting.attendees
                        ]
                    ) for meeting in meetings
                ]




@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_user(self, name: str, email: str) -> User:
        # Create a new user
        with Session() as session:
            existing_user = session.query(UserModel).filter(UserModel.email == email).first()
            if existing_user:
                raise ValueError(f"User with email {email} already exists")
                
            new_user = UserModel(name=name, email=email)
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            return User(id=new_user.id, name=new_user.name, email=new_user.email, meetings=[])
    
    @strawberry.mutation
    def create_meeting(self, title: str, time: str, content: str) -> Meeting:
        # Create a new meeting
        with Session() as session:
            existing_meeting = session.query(MeetingModel).filter(MeetingModel.title == title).first()
            if existing_meeting:
                raise ValueError(f"Meeting with title '{title}' already exists")
                
            time_obj = datetime.datetime.strptime(time, "%H:%M").time() if time else None
            new_meeting = MeetingModel(title=title, time=time_obj, content=content)
            session.add(new_meeting)
            session.commit()
            session.refresh(new_meeting)
            return Meeting(id=new_meeting.id, title=new_meeting.title, time=str(new_meeting.time) if new_meeting.time else "", content=new_meeting.content, attendees=[])
    
    @strawberry.mutation
    def add_user_to_meeting(self, user_id: int, meeting_id: int) -> Meeting:
        # Add user to meeting
        with Session() as session:
            user = session.get(UserModel, user_id)
            if not user:
                raise ValueError(f"User with id={user_id} not found")
                
            meeting = session.get(MeetingModel, meeting_id)
            if not meeting:
                raise ValueError(f"Meeting with id={meeting_id} not found")
            
            if user in meeting.attendees:
                raise ValueError(f"User is already attendee")
                
            meeting.attendees.append(user)
            session.commit()
            
            return Meeting(
                id=meeting.id,
                title=meeting.title,
                time=str(meeting.time) if meeting.time else "",
                content=meeting.content,
                attendees=[
                    User(
                        id=attendee.id, 
                        name=attendee.name, 
                        email=attendee.email,
                        meetings=[]
                    ) for attendee in meeting.attendees
                ]
            )
    
    @strawberry.mutation
    def remove_user_from_meeting(self, user_id: int, meeting_id: int) -> Meeting:
        # Remove user from meeting
        with Session() as session:
            user = session.get(UserModel, user_id)
            if not user:
                raise ValueError(f"User with id={user_id} not found")
                
            meeting = session.get(MeetingModel, meeting_id)
            if not meeting:
                raise ValueError(f"Meeting with id={meeting_id} not found")
            
            if user not in meeting.attendees:
                raise ValueError(f"User is not an attendee")
                
            meeting.attendees.remove(user)
            session.commit()
            
            return Meeting(
                id=meeting.id,
                title=meeting.title,
                time=str(meeting.time) if meeting.time else "",
                content=meeting.content,
                attendees=[
                    User(
                        id=attendee.id, 
                        name=attendee.name, 
                        email=attendee.email,
                        meetings=[]  # Пустой список для избежания рекурсии
                    ) for attendee in meeting.attendees
                ]
            )
    
    @strawberry.mutation
    def remove_user(self, user_id: int) -> str:
        # Remove user
        with Session() as session:
            user = session.get(UserModel, user_id)
            if not user:
                raise ValueError(f"User with id={user_id} not found")
            
            session.delete(user)
            session.commit()
            
            return f"User with id={user_id} was successfully deleted"
    
    @strawberry.mutation
    def remove_meeting(self, meeting_id: int) -> str:
        # Remove meeting
        with Session() as session:
            meeting = session.get(MeetingModel, meeting_id)
            if not meeting:
                raise ValueError(f"Meeting with id={meeting_id} not found")
            
            session.delete(meeting)
            session.commit()
            
            return f"Meeting with id={meeting_id} was successfully deleted"
        
schema = strawberry.Schema(query=Query, mutation=Mutation)