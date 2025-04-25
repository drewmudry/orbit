from django.core.management.base import BaseCommand
from django.db import transaction
from core.users.models import User
from core.organizations.models import Organization, Profile, Group, Membership
import random

class Command(BaseCommand):
    help = 'Seeds the database with initial data'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')
        
        # Clear existing data
        Membership.objects.all().delete()
        Group.objects.all().delete()
        Profile.objects.all().delete()
        Organization.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        
        # Create NBA organization
        nba = Organization.objects.create(name="National Basketball Association")
        self.stdout.write(f'Created organization: {nba.name}')
        
        # Create teams (groups)
        teams = [
            "Los Angeles Lakers",
            "Golden State Warriors",
            "Phoenix Suns",
            "Boston Celtics",
            "Miami Heat",
            "Dallas Mavericks"
        ]
        
        created_teams = {}
        for team_name in teams:
            team = Group.objects.create(name=team_name, organization=nba)
            created_teams[team_name] = team
            self.stdout.write(f'Created team: {team.name}')
        
        # Create users and their profiles
        users_data = [
            {
                "email": "lebron@example.com",
                "first_name": "LeBron",
                "last_name": "James",
                "team": "Los Angeles Lakers",
                "is_admin": True
            },
            {
                "email": "curry@example.com",
                "first_name": "Stephen",
                "last_name": "Curry",
                "team": "Golden State Warriors",
                "is_admin": True
            },
            {
                "email": "booker@example.com",
                "first_name": "Devin",
                "last_name": "Booker",
                "team": "Phoenix Suns",
                "is_admin": True
            },
            {
                "email": "tatum@example.com",
                "first_name": "Jayson",
                "last_name": "Tatum",
                "team": "Boston Celtics",
                "is_admin": True
            },
            {
                "email": "butler@example.com",
                "first_name": "Jimmy",
                "last_name": "Butler",
                "team": "Miami Heat",
                "is_admin": True
            },
            {
                "email": "doncic@example.com",
                "first_name": "Luka",
                "last_name": "Doncic",
                "team": "Dallas Mavericks",
                "is_admin": True
            },
            {
                "email": "davis@example.com",
                "first_name": "Anthony",
                "last_name": "Davis",
                "team": "Los Angeles Lakers",
                "is_admin": False
            },
            {
                "email": "thompson@example.com",
                "first_name": "Klay",
                "last_name": "Thompson",
                "team": "Golden State Warriors",
                "is_admin": False
            },
            {
                "email": "silver@example.com",
                "first_name": "Adam",
                "last_name": "Silver",
                "team": None,  # NBA Commissioner, not tied to a specific team
                "is_admin": True
            }
        ]
        
        created_profiles = {}
        for user_data in users_data:
            user = User.objects.create_user(
                email=user_data["email"],
                password="password123",  # Simple password for testing
                first_name=user_data["first_name"],
                last_name=user_data["last_name"]
            )
            
            full_name = f"{user.first_name} {user.last_name}"
            profile = Profile.objects.create(
                user=user,
                organization=nba,
                name=full_name,
                email=user.email,
                is_admin=user_data["is_admin"]
            )
            
            created_profiles[user.email] = profile
            self.stdout.write(f'Created user and profile: {full_name}')
            
            # Add to team if specified
            if user_data["team"]:
                team = created_teams[user_data["team"]]
                
                # For demonstration, randomly assign permissions to non-admins
                permissions = {
                    "is_admin": user_data["is_admin"],
                    "announce_can_create": user_data["is_admin"] or random.choice([True, False]),
                    "sign_can_create": user_data["is_admin"] or random.choice([True, False])
                }
                
                Membership.objects.create(
                    profile=profile,
                    group=team,
                    **permissions
                )
                self.stdout.write(f'Added {full_name} to {team.name}')
        
        # Add some cross-team memberships (players who moved teams)
        # For example, add LeBron to his former teams
        lebron_profile = created_profiles["lebron@example.com"]
        for team_name in ["Miami Heat", "Boston Celtics"]:
            Membership.objects.create(
                profile=lebron_profile,
                group=created_teams[team_name],
                is_admin=False,
                announce_can_create=True,
                sign_can_create=False
            )
            self.stdout.write(f'Added LeBron James to {team_name} (former team)')
        
        # Make Adam Silver a member of all teams (as commissioner)
        silver_profile = created_profiles["silver@example.com"]
        for team_name, team in created_teams.items():
            Membership.objects.create(
                profile=silver_profile,
                group=team,
                is_admin=True,
                announce_can_create=True,
                sign_can_create=True
            )
            self.stdout.write(f'Added Adam Silver to {team_name} (as commissioner)')
        
        # Create a superuser for admin access
        if not User.objects.filter(email="admin@example.com").exists():
            User.objects.create_superuser(
                email="drew@creovia.io",
                password="qqn"
            )
            self.stdout.write(f'Created superuser: drew@creovia.io')
        
        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))