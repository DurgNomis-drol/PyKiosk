echo "=================================="
echo "=== Install script for PyKiosk ==="
echo "=================================="
echo "Setting up and installing dependancies..."
sudo dnf install python3-pip chromium -y
echo "Done!"
echo "Installing PyKiosk..."
sudo chmod +x driver/chromedriver
sudo cp driver/chromedriver /usr/local/bin/
sudo chmod 775 ./driver/chromedriver
#Chrome is the core browser used for the kiosk
sudo chmod 775 ./*
#Make sure every file has the 775 permission
echo "Done!"
echo "Installing python modules..."
sudo pip install selenium flask flask_httpauth, flask-restful
echo "Done!"
echo "Making it launch on startup..."
cat <<EOT >> pykiosk.desktop
[Desktop Entry]
Type=Application
Exec=python /home/$HOME/PyKiosk/app.py
X-GNOME-Autostart-enabled=true
Name=PyKiosk
Comment=PyKiosk python based webkiosk
EOT
sudo cp pykiosk.desktop $HOME/.config/autostart/
echo "Auto start have been successfully setup."
echo "Enabling autologin for $USER"
sudo sed '/\[daemon\]/a AutomaticLogin=$USER'
sudo sed '/\[daemon\]/a AutomaticLoginEnable=True'
echo "Autologin enabled!"
echo "You have to manually change orientation, because xrandr cannot."
echo "Done!"
echo "Please reboot your system now by typing 'reboot'"