import cmd
from oldschool_management_tools.oldschool_management_tools import parse_day, show_day_sched, prompt_day_tasks, fill_prep, wipe_prep



class MgmtToolsCmd(cmd.Cmd):
    intro = "Welcome to Old School Management Tools"
    prompt = "(mgmt) "

    def do_prompt_tasks(self, day):
        parsed_day = parse_day(day)
        prompt_day_tasks(parsed_day)

    def do_show_sched(self, day):
        parsed_day = parse_day(day)
        show_day_sched(parsed_day)

    def do_fill_prep(self, day):
        parsed_day = parse_day(day)
        fill_prep(parsed_day)

    def do_wipe_prep(self, day):
        parsed_day = parse_day(day)
        wipe_prep(parsed_day)

    def do_die(self, args):
        return True


    def do_exit(self, args):
        return True

    def do_EOF(self, args):
        return True


MgmtToolsCmd().cmdloop()
exit(0)
