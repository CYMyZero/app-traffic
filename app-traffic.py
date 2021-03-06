from javax.swing import JPanel, JTextField, JButton, JLabel, BoxLayout
from burp import IBurpExtender, ITab

import ctypes  
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
    def set_key(self, ip, value):  
        subprocess.Popen('taskkill /f /im iexplore.exe >nul 2>&1', shell=True)
        subprocess.Popen('reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer /d "'+str(ip)+'" /f', shell=True)
        subprocess.Popen('reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d '+str(value)+' /f', shell=True)
        subprocess.Popen('ping -n 5 127.0.0.1 >nul', shell=True)
        subprocess.Popen('start iexplore.exe http://burp', shell=True)

    def set_sys_proxy(self,on_off):
        if on_off:
            self.set_key(self.target_host.text, 1)   
        else:
            self.set_key('', 0)  
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
