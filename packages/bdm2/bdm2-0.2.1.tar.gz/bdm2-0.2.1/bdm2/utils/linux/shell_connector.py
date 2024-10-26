import re

import paramiko


class ShellHandler:
    """
    class for opening linux shell
    """

    def __init__(self, host, user, psw):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(host, username=user, key_filename=psw, port=22)

        channel = self.ssh.invoke_shell()
        self.stdin = channel.makefile('wb')
        self.stdout = channel.makefile('r')

    def __del__(self):
        self.ssh.close()

    def execute(self, cmd):
        """

        :param cmd: the command to be executed on the remote computer
        :examples:  execute('ls')
                    execute('finger')
                    execute('cd folder_name')
        """
        cmd = cmd.strip('\n')
        self.stdin.write(cmd + '\n')
        finish = 'end of stdOUT buffer. finished with exit status'
        echo_cmd = 'echo {} $?'.format(finish)
        self.stdin.write(echo_cmd + '\n')
        shin = self.stdin
        self.stdin.flush()

        shout = []
        sherr = []
        exit_status = 0
        for line in self.stdout:
            if str(line).startswith(cmd) or str(line).startswith(echo_cmd):
                # up for now filled with shell junk from stdin
                shout = []
            elif str(line).startswith(finish):
                # our finish command ends with the exit status
                exit_status = int(str(line).rsplit(maxsplit=1)[1])
                if exit_status:
                    # stderr is combined with stdout.
                    # thus, swap sherr with shout in a case of failure.
                    sherr = shout
                    shout = []
                break
            else:
                # get rid of 'coloring and formatting' special characters
                shout.append(re.compile(r'(\x9B|\x1B\[)[0-?]*[ -/]*[@-~]').sub('', line).
                             replace('\b', '').replace('\r', ''))

        # first and last lines of shout/sherr contain a prompt
        if shout and echo_cmd in shout[-1]:
            shout.pop()
        if shout and cmd in shout[0]:
            shout.pop(0)
        if sherr and echo_cmd in sherr[-1]:
            sherr.pop()
        if sherr and cmd in sherr[0]:
            sherr.pop(0)

        return shin, shout, sherr


if __name__ == '__main__':
    print()
    # TODO: make shell recall example
    # import pandas as pd
    # from io import StringIO
    #
    #
    # host = "34.216.244.169"
    # user = "ubuntu"
    # key = r"\\datasets\chikens\configs\aws_pem\ms_bookawheelkey.pem"
    #
    # # connection and required defining permission
    # shell = ShellHandler(host=host, psw=key, user=user)
    # shell.stdin.write("sudo su " + '\n')
    #
    # TEST_ENGINE = "_v4.10.7.45_CGTHBG_Cobb_male_2704_final"
    # cmd_go2_engines = f'cd /home/ubuntu/efs/efs/engines/{TEST_ENGINE}'
    # _ex1 = shell.execute(cmd=cmd_go2_engines)
    #
    # cmd_ls = 'ls -1\n'
    # _ex1 = shell.execute(cmd=cmd_ls)[1]
    # stat_file = [i for i in _ex1 if "Generated_Statistics" in i][0]
    # cmd_read_stat_file = f"cat {stat_file}"
    # res = shell.execute(cmd=cmd_read_stat_file)[1]
    #
    #
    # line = ''
    # for num, _ in enumerate(res):
    #     line += _
    #
    # stat_df = pd.read_csv(StringIO(line), sep=';')

    # if num == 0:
    #     continue
    # part_stat = pd.read_csv(StringIO(_), sep=';')
    # break
    # part_stat = pd.DataFrame(StringIO(_))
    # initial_stat_df = initial_stat_df.iloc[num, :] = part_stat #pd.concat([initial_stat_df, part_stat])

    # # changing data
    # devices_search4 = [
    #     # '00339A',
    #                    '00340A',
    #                    '00342A',
    #                    '00341A',
    #                    '00345A',
    #                    '00346A',
    #                    '00325A',
    #                    '00326A']
    #
    # # start dir for searching for dome files
    # cmd_go2cvres_folder_ = 'cd /home/ubuntu/efs/efs/engines'
    # # this linux command allows to get list of files\dirs, normal one list
    # cmd_ls = 'ls -1\n'
    # # your regex pattern for search
    # pattern = re.compile(f'.*(?P<outpud_folder>output_tmp.*.zip)')
    # # changing download command
    # original_download_command = r'curl -T /home/ubuntu/efs/efs/cvres/DEVICE/CY_HA_CO/AGE_SESS/ZIPFILE ' \
    #                             r'ftp://user365508:JIe0Xd9SCAme@194.63.141.39/device_volume_diff/REPLACABLE'
    # # MAIN LOOP
    # for device in devices_search4:
    #     cmd_go2cvres_folder = cmd_go2cvres_folder_ + f'/{device}'
    #     _ex1 = shell.execute(cmd=cmd_go2cvres_folder)
    #     _ex2 = shell.execute(cmd=cmd_ls)
    #     for cy_ha_co in _ex2[1]:
    #         if 'root' in cy_ha_co:
    #             continue
    #         cy_ha_co = cy_ha_co.strip('\n')
    #         if cy_ha_co.endswith('-5'):
    #             # break
    #             cmd_go2cy_ha_co = cmd_go2cvres_folder + f'/{cy_ha_co}'
    #             _ex3 = shell.execute(cmd=cmd_go2cy_ha_co)
    #             _ex4 = shell.execute(cmd=cmd_ls)
    #             for age_sess_ in _ex4[1]:
    #                 if 'root' in age_sess_:
    #                     continue
    #                 age_sess = age_sess_.strip('\n')
    #                 if age_sess.endswith('.12') or age_sess.endswith('.10'):
    #                     # continue
    #                     cmd_go2resfolder = cmd_go2cy_ha_co + f'/{age_sess}'
    #                     _ex5 = shell.execute(cmd=cmd_go2resfolder)
    #                     _ex6 = shell.execute(cmd=cmd_ls)
    #                     outputs = [i.strip('\n') for i in _ex6[1] if pattern.match(i)]
    #                     for archive in outputs:
    #                         print('downloading',  cy_ha_co,  device, archive)
    #                         cmd_download = original_download_command.replace('DEVICE', device)
    #                         cmd_download = cmd_download.replace('CY_HA_CO', cy_ha_co)
    #                         cmd_download = cmd_download.replace('AGE_SESS', age_sess)
    #                         cmd_download = cmd_download.replace('ZIPFILE', archive)
    #                         archive_save_filename = cy_ha_co + '_' + device + '_' + archive
    #                         cmd_download = cmd_download.replace('REPLACABLE', archive_save_filename)
    #                         _ex7 = shell.execute(cmd=cmd_download)
    #
    #
    #
    #         # break
    #     # for
    #     # line.strip('\n')
    #     # break
    #
    # #--------
    #
    #
    # # _ex = shell.execute(cmd=cmd_go2cvres_folder)
    # # _ex1 = shell.execute(cmd=cmd_ls)
    # # print()
