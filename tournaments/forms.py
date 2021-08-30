from django import forms
from django.core.exceptions import ValidationError
from .models import TeamsModel

# create your variables here
game_type_choices = (('PUBG', 'PUBG'),
                     ('Sea of Theves', 'Sea of Theves'),
                     ('Call of duty', 'Call of Duty'))
filter_game_type_choices = (('PUBG', 'PUBG'),
                            ('Sea of Theves', 'Sea of Theves'),
                            ('Call of duty', 'Call of Duty'),
                            ('All', 'All'))

team_type_choices = (('1v1', '1v1'),
                     ('2v2', '2v2'),
                     ('4v4', '4v4'))

fee_type = (('PAID', 'PAID'),
            ('FREE', 'FREE'),
            ('All', 'All'))


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'


# Custom validators
def team_is_exists(team_name):
    team = TeamsModel.objects.filter(name=team_name)
    if not team.exists():
        raise ValidationError('No team in this name exists.')


# Create your form classes here


class TournamentForm(forms.Form):
    name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'placeholder': 'Enter your tournament name'
    }))
    game_type = forms.ChoiceField(choices=game_type_choices)
    team_type = forms.ChoiceField(choices=team_type_choices)
    slots = forms.CharField(max_length=3, widget=forms.TextInput(attrs={
        'placeholder': 'Total number of teams'
    }))
    fee = forms.IntegerField(label='Entry Fee', widget=forms.NumberInput(attrs={
        'placeholder': 'Entry fee per team'
    }))
    first_prize = forms.CharField(max_length=4,
                                  label='First Prize', widget=forms.TextInput(attrs={
            'placeholder': 'Enter amount for first prize '
        }))
    second_prize = forms.CharField(max_length=4,
                                   label='Second Prize', widget=forms.TextInput(attrs={
            'placeholder': 'Enter amount for second prize '
        }))
    third_prize = forms.CharField(max_length=4,
                                  label='Third Prize', widget=forms.TextInput(attrs={
            'placeholder': 'Enter amount for third prize '
        }))
    registration_deadline = forms.DateTimeField(widget=DateInput)
    start_date = forms.DateField(widget=DateInput)
    start_time = forms.TimeField(widget=TimeInput)
    tournament_image = forms.ImageField()
    description = forms.CharField(widget=forms.Textarea(attrs={
        'row': 5,
        'cols': 20,
        'id': 'description',
        'placeholder': '''
        Please enter full description for this tournament.
    -----------------------
    Rules:
        1. Cheaters will be banned and disqualified.
        2. If one member cheats then the team will
        be disqualified.
        3. Disqualified team will not get their money
        back.
        
        
        
        '''

    }))


class TeamsForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'placeholder': 'Enter Your team name',

    }))
    player1 = forms.CharField(max_length=10, required=False, widget=forms.TextInput(attrs={
        'placeholder': 'ex:0981298651',

    }))
    player2 = forms.CharField(max_length=10, required=False, widget=forms.TextInput(attrs={
        'placeholder': 'ex:0981298651',

    }))
    player3 = forms.CharField(max_length=10, required=False, widget=forms.TextInput(attrs={
        'placeholder': 'ex:0981298651',

    }))
    bkash_payment_number = forms.IntegerField(widget=forms.TextInput(attrs={
        'placeholder': 'ex:019925****1'
    }))
    bkash_trxid = forms.IntegerField(widget=forms.TextInput(attrs={
        'placeholder': 'ex:8HE9JQQB7F'
    }))


class EditTournamentForm(forms.Form):
    edit_name = forms.CharField(max_length=30, help_text='Enter your tournament name', required=False)
    edit_game_type = forms.ChoiceField(choices=game_type_choices, required=False)
    edit_team_type = forms.ChoiceField(choices=team_type_choices, required=False)
    edit_slots = forms.CharField(max_length=3, help_text='Total number of teams', label='Total teams', required=False)
    edit_fee = forms.CharField(max_length=3, help_text='Enter 0 for free entry.', label='Entry Fee', required=False)
    edit_first_prize = forms.CharField(max_length=4, help_text='First prize money. Enter 0 for no prize.',
                                       label='First Prize', required=False)
    edit_second_prize = forms.CharField(max_length=4, help_text='Second prize money. Enter 0 for no prize.',
                                        label='Second Prize', required=False)
    edit_third_prize = forms.CharField(max_length=4, help_text='Third prize money. Enter 0 for no prize.',
                                       label='Third Prize', required=False)
    edit_registration_deadline = forms.DateField(widget=DateInput,
                                                 required=False)
    edit_start_date = forms.DateField(widget=DateInput, required=False)
    edit_start_time = forms.TimeField(widget=TimeInput, required=False)
    edit_tournament_image = forms.ImageField(required=False)

    edit_description = forms.CharField(widget=forms.Textarea(attrs={
        'row': 5,
        'cols': 20
    }), required=False)


class TournamentFilterForm(forms.Form):
    money_type = forms.ChoiceField(choices=fee_type, required=False)
    type_of_game = forms.ChoiceField(choices=filter_game_type_choices, required=False)
    date = forms.DateField(widget=DateInput, required=False)


# Room id and password form
class RoomForm(forms.Form):
    room_id = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'placeholder': 'Enter room id'
    }))
    room_password = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'placeholder': 'Enter room password'
    }))


# Winner add form

class WinnerForm(forms.Form):
    result_image = forms.ImageField()
    first_team = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'placeholder': "Enter first placed team's name"
    }), validators=[team_is_exists])
    second_team = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'placeholder': "Enter second placed team's name"
    }), validators=[team_is_exists])
    third_team = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'placeholder': "Enter third placed team's name"
    }), validators=[team_is_exists])
