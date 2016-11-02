Summary: A script to monitor a system for abnormal conditions, and log data
Name: snoopy
Version: 1.0.0
Release: 0
License: MIT
Group: Applications/System
BuildRoot: %{_topdir}/%{name}-%{version}-%{release}-build
BuildArch: noarch
Requires: bash cronie
#Source: http://metalab.unc.edu/pub/Linux/utils/disk-management/eject-2.0.2.tar.gz
#Patch: eject-2.0.2-buildroot.patch
#BuildRoot: /var/tmp/%{name}-buildroot

%description
The snoopy script runs on an interval, and monitors the system for errant
conditions - high load, high swap usage, high httpd or MySQL utilization.

When errant conditions are detected, certain information is dumped to a file
for later inspection.

%prep
rm -rf ${RPM_BUILD_DIR}/snoopy
git clone https://github.com/JackKnifed/snoopy.git ${RPM_BUILD_DIR}/snoopy
[[ $? -ne 0 ]] && exit $?

%build

%install
install -d /var/log/snoopy
mkdir -p /usr/local/bin /etc
install -m 755 ${RPM_BUILD_DIR}/snoopy/snoopy.conf /etc/snoopy.conf
install -m 0700 ${RPM_BUILD_DIR}/snoopy/snoopy /usr/local/bin/snoopy
install -m 0700 ${RPM_BUILD_DIR}/snoopy/snoopy.cron /etc/cron.d/snoopy.cron
touch /etc/plbakeloadwatchinstalled

%post
[[ /root/loadwatch/checklog -f ]] && mv /root/loadwatch/checklog /var/log/snoopy.log
[[ /root/loadwatch -d ]] && rsync /root/loadwatch /var/log/snoopy
rm -rf /root/loadwatch
rm -f /root/bin/loadwatch


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)

%dir /var/log/snoopy
%config /etc/snoopy.conf
/usr/local/bin/snoopy
/etc/cron.d/snoopy.cron

%changelog
* Tue Nov 01 2016 Jack Hayhurst <jhayhurst@liquidweb.com> 
- Wrote inital build script and changelog.
