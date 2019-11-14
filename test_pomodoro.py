import pytest
from unittest.mock import patch

from pomodoro import setup_arguments
from pomodoro import wait_input
from pomodoro import timer

from progressbar import progress_bar

@patch('sys.argv', ['UNUSED','-d'])
def test_setup_arguments():
    args = setup_arguments()

    assert args.debug == True
    assert args.name == 'My Pomodoro Task'
    assert args.pomodoro == .5
    assert args.short_break_duration == .1
    assert args.long_break_duration == .2

@patch("builtins.input", side_effect=['test', 'QUit', '\n'])
def test_wait_input(inp):
    assert wait_input() is None
    with pytest.raises(SystemExit):
        assert wait_input()
    assert wait_input() is None

@patch('time.sleep', return_value=None)
@patch('pomodoro.progress_bar', autospec=True)
def test_timer(prg, slp):
    timer(2, 'test')
    #print(prg.mock_calls[0][2]['progress'])
    assert prg.mock_calls[0][2]['progress'] == 100
    assert prg.mock_calls[1][2]['progress'] == 50
    assert prg.mock_calls[2][2]['progress'] == 0