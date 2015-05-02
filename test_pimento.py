'''
Test suite for pimento
'''


# [ Imports ]
# [ -Third Party ]
import pexpect
# [ -Project ]
import pimento


# [ Helpers ]
def expect_color_menu_prompt(process):
    process.expect_exact('which color?')
    process.expect_exact('  red')
    process.expect_exact('  blue')
    process.expect_exact('  green')
    process.expect_exact('  black')
    process.expect_exact('  grey')
    process.expect_exact('  white')
    process.expect_exact('Please select one: ')


def get_color_menu_process():
    p = pexpect.spawn('python test_pimento.py --colors', timeout=1)
    expect_color_menu_prompt(p)
    return p


def expect_menu_prompt(process):
    process.expect_exact('yes or no?')
    process.expect_exact('  yes')
    process.expect_exact('  no')
    process.expect_exact('Please choose: ')


def get_menu_process():
    p = pexpect.spawn('python test_pimento.py --yn', timeout=1)
    expect_menu_prompt(p)
    return p


# [ Tests ]
def test_menu_accepts_full_response():
    # yes
    p = get_menu_process()
    p.sendline('yes')
    p.expect('Result was yes')
    # no
    p = get_menu_process()
    p.sendline('no')
    p.expect('Result was no')


def test_menu_rejects_unmatching_response():
    # yes
    p = get_menu_process()
    p.sendline('maybe')
    p.expect_exact('[!] "maybe" does not match any of the valid choices.')
    expect_menu_prompt(p)
    p.sendline('yes')
    p.expect('Result was yes')
    # no
    p = get_menu_process()
    p.sendline('maybe')
    p.expect_exact('[!] "maybe" does not match any of the valid choices.')
    expect_menu_prompt(p)
    p.sendline('no')
    p.expect('Result was no')


def test_menu_rejects_no_response():
    # yes
    p = get_menu_process()
    p.sendline('')
    p.expect_exact('[!] an empty response is not valid.')
    expect_menu_prompt(p)
    p.sendline('yes')
    p.expect('Result was yes')
    # no
    p = get_menu_process()
    p.sendline('')
    p.expect_exact('[!] an empty response is not valid.')
    expect_menu_prompt(p)
    p.sendline('no')
    p.expect('Result was no')


def test_menu_accepts_partial_response():
    # yes
    p = get_menu_process()
    p.sendline('y')
    p.expect('Result was yes')
    p = get_menu_process()
    p.sendline('ye')
    p.expect('Result was yes')
    # no
    p = get_menu_process()
    p.sendline('n')
    p.expect('Result was no')


def test_menu_rejects_multiple_matches():
    # blue
    p = get_color_menu_process()
    p.sendline('b')
    p.expect_exact('[!] "b" matches multiple choices:')
    p.expect_exact('[!]   blue')
    p.expect_exact('[!]   black')
    p.expect_exact('[!] Please specify your choice further.')
    expect_color_menu_prompt(p)
    p.sendline('bl')
    p.expect_exact('[!] "bl" matches multiple choices:')
    p.expect_exact('[!]   blue')
    p.expect_exact('[!]   black')
    p.expect_exact('[!] Please specify your choice further.')
    p.sendline('blu')
    p.expect('Result was blue')
    # black
    p = get_color_menu_process()
    p.sendline('bla')
    p.expect('Result was black')


# [ Manual Interaction ]
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--yn', help='yes or no prompt',
                        action='store_true')
    group.add_argument('--colors', help='colors prompt',
                        action='store_true')
    args = parser.parse_args()
    if args.yn:
        result = pimento.menu("yes or no?", ['yes', 'no'], "Please choose: ")
    elif args.colors:
        result = pimento.menu(
            "which color?",
            [
                'red', 'blue', 'green',
                'black', 'grey', 'white'
             ],
            "Please select one: "
        )
    print 'Result was {}'.format(result)
