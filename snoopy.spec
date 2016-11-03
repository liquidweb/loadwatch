Summary: A script to monitor a system for abnormal conditions, and log data
Name: snoopy
Version: 1.0.0
Release: 0
License: MIT
Group: Applications/System
BuildRoot: %{_topdir}/%{name}-%{version}-%{release}-build
BuildArch: noarch
Requires: bash, cronie
#Source: https://github.com/JackKnifed/snoopy/archive/master.tar.gz

%description
The snoopy script runs on an interval, and monitors the system for errant
conditions - high load, high swap usage, high httpd or MySQL utilization.

When errant conditions are detected, certain information is dumped to a file
for later inspection.

%prep
rm -rf ${RPM_BUILD_DIR}/snoopy
curl -L https://github.com/jackknifed/snoopy/archive/master.tar.gz | tar xz

%build

%install
mkdir -p %{buildroot}/usr/local/bin %{buildroot}/etc/cron.d %{buildroot}/var/log/snoopy
install -m 0700 ${RPM_BUILD_DIR}/snoopy-master/snoopy %{buildroot}/usr/local/bin/snoopy
install -m 755 ${RPM_BUILD_DIR}/snoopy-master/snoopy.conf %{buildroot}/etc/snoopy.conf
install -m 0700 ${RPM_BUILD_DIR}/snoopy-master/snoopy.cron %{buildroot}/etc/cron.d/snoopy.cron
touch %{buildroot}/etc/plbakeloadwatchinstalled

%post
[[ /root/loadwatch/checklog -f ]] && mv /root/loadwatch/checklog /var/log/snoopy.log
[[ /root/loadwatch -d ]] && rsync /root/loadwatch /var/log/snoopy
rm -rf /root/loadwatch
rm -f /root/bin/loadwatch


%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)

%dir /var/log/snoopy
%config /etc/snoopy.conf
/usr/local/bin/snoopy
/etc/cron.d/snoopy.cron
/etc/plbakeloadwatchinstalled

%changelog
* Tue Nov 01 2016 Jack Hayhurst <jhayhurst@liquidweb.com> 
- Wrote inital build script and changelog.
