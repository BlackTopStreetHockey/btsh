import pytest
from django.core.exceptions import ValidationError

from api.utils.testing import BaseTest
from users.models import UserSeasonRegistration


class TestUserModel(BaseTest):
    def test_to_str(self, wgretzky):
        assert str(wgretzky) == 'Wayne Gretzky - thegr81@btsh.org'


class TestUserSeasonRegistrationModel(BaseTest):
    def test_clean(self, user_season_registration_factory, cmcdavid, season_2024, corlears_hookers):
        with pytest.raises(ValidationError):
            user_season_registration_factory(
                user=None,
                season=None,
                team=None,
                is_captain=None,
                position=None,
                signature=None,
                location=None,
                interested_in_reffing=None,
                interested_in_opening_closing=None,
                interested_in_other=None,
                interested_in_next_year=None,
                mid_season_party_ideas=None,
            )

        with pytest.raises(ValidationError) as e:
            user_season_registration_factory(
                user=cmcdavid,
                season=season_2024,
                team=corlears_hookers,
                is_captain=True,
                position=UserSeasonRegistration.FORWARD,
                signature='Michael Scott',
                location=UserSeasonRegistration.QUEENS,
                interested_in_reffing=False,
                interested_in_opening_closing=False,
                interested_in_other=None,
                interested_in_next_year=False,
                mid_season_party_ideas=None,
            )
        assert e.value.message_dict == {'signature': ['Signature must match the user\'s full name.']}

    def test_to_str(self, wgretzky_2024_season_registration):
        assert str(wgretzky_2024_season_registration) == (
            'Wayne Gretzky - thegr81@btsh.org - 03/31/2024 - 10/31/2024 Season - Corlears Hookers'
        )

    def test_user_season_team_uniq(self, user_season_registration_factory, wgretzky_2024_season_registration):
        with pytest.raises(ValidationError) as e:
            user_season_registration_factory(
                user=wgretzky_2024_season_registration.user,
                season=wgretzky_2024_season_registration.season,
                team=wgretzky_2024_season_registration.team,
                is_captain=True,
                position=UserSeasonRegistration.FORWARD,
                signature='Wayne Gretzky',
                location=UserSeasonRegistration.BRONX,
                interested_in_reffing=False,
                interested_in_opening_closing=False,
                interested_in_other=None,
                interested_in_next_year=False,
                mid_season_party_ideas=None,
            )
        assert e.value.message_dict == {
            '__all__': ['User season registration with this User, Season and Team already exists.']
        }
