from javax.swing import JPanel, JTextField, JButton, JLabel, BoxLayout
from burp import IBurpExtender, ITab

import subprocess

class BurpExtender(IBurpExtender, ITab):

    def registerExtenderCallbacks(self, callbacks):
        self.callbacks = callbacks
        self.isEnabled = False

        callbacks.setExtensionName('app-traffic')
        callbacks.addSuiteTab(self)


    # Called on "Enable" button click to spin up the API Gateway

    def enableGateway(self, event):
        self.isEnabled = True
        self.set_sys_proxy(True)
        self.enable_button.setEnabled(False)
        self.target_host.setEnabled(False)
        self.disable_button.setEnabled(True)
        return

    # Called on "Disable" button click to delete API Gateway
    def disableGateway(self, event):
        self.isEnabled = False
        self.set_sys_proxy(False)
        self.enable_button.setEnabled(True)
        self.target_host.setEnabled(True)
        self.disable_button.setEnabled(False)
        return
    # Tab name
    def getTabCaption(self):
        return 'app-traffic'

    def set_sys_proxy(self,on_off):
        if on_off:
            on_off="1"
            ip=self.target_host.text
        else:
            on_off="0"
            ip=""
        subprocess.Popen('reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d '+on_off+' /f', shell=True)
        subprocess.Popen('reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer /d "'+ip+'" /f', shell=True)
        subprocess.Popen('taskkill /im explorer.exe /f&&ping -n 2 127.0.0.1 > nul&&start c:\windows\explorer.exe', shell=True)

    # Layout the UI
    def getUiComponent(self):

        self.panel = JPanel()

        self.main = JPanel()
        self.main.setLayout(BoxLayout(self.main, BoxLayout.Y_AXIS))


        self.target_host_panel = JPanel()
        self.main.add(self.target_host_panel)
        self.target_host_panel.setLayout(
            BoxLayout(self.target_host_panel, BoxLayout.X_AXIS))
        self.target_host_panel.add(JLabel('Listen Prot:'))
        self.target_host = JTextField('127.0.0.1:8080', 25)
        self.target_host_panel.add(self.target_host)

        self.buttons_panel = JPanel()
        self.main.add(self.buttons_panel)
        self.buttons_panel.setLayout(
            BoxLayout(self.buttons_panel, BoxLayout.X_AXIS))
        self.enable_button = JButton('Enable', actionPerformed= self.enableGateway)
        self.buttons_panel.add(self.enable_button)
        self.disable_button = JButton('Disable', actionPerformed= self.disableGateway)
        self.buttons_panel.add(self.disable_button)
        self.disable_button.setEnabled(False)


        self.panel.add(self.main)
        return self.panel
