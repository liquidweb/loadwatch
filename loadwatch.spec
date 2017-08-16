
%global tardir loadwatch-master
Summary: A script to monitor a system for abnormal conditions, and log data
Name: loadwatch
Version: 0.1.0
Release: 0
License: MIT
Group: Applications/System
BuildRoot: %{_topdir}/%{name}-%{version}-%{release}-build
BuildArch: noarch
Requires: bash, cronie, lynx
#Source: https://github.com/JackKnifed/loadwatch/archive/master.tar.gz

%description
The loadwatch script runs on an interval, and monitors the system for errant
conditions - high load, high swap usage, high httpd or MySQL utilization.

When errant conditions are detected, certain information is dumped to a file
for later inspection.

%prep
rm -rf ${RPM_BUILD_DIR}/loadwatch
curl -L https://github.com/jackknifed/loadwatch/archive/master.tar.gz | tar xz

%build

%install
mkdir -p \
  %{buildroot}/usr/local/lp/bin \
  %{buildroot}/etc/default \
  %{buildroot}/etc/cron.d \
  %{buildroot}/var/log/loadwatch
install -m 0700 ${RPM_BUILD_DIR}/loadwatch-master/loadwatch %{buildroot}/usr/local/lp/bin/loadwatch
install -m 755 ${RPM_BUILD_DIR}/loadwatch-master/loadwatch.env %{buildroot}/etc/default/loadwatch
install -m 0700 ${RPM_BUILD_DIR}/loadwatch-master/loadwatch.cron %{buildroot}/etc/cron.d/loadwatch.cron
touch %{buildroot}/etc/plbakeloadwatchinstalled

%post
[[ /root/loadwatch/checklog -f ]] && mv /root/loadwatch/checklog /var/log/loadwatch.log
[[ /root/loadwatch -d ]] && rsync /root/loadwatch /var/log/loadwatch
rm -rf /root/loadwatch
rm -f /root/bin/loadwatch


%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)

%dir /var/log/loadwatch
%config(noreplace) /etc/default/loadwatch
/usr/local/lp/bin/loadwatch
/etc/cron.d/loadwatch.cron
/etc/plbakeloadwatchinstalled

%changelog
* Tue Nov 01 2016 Jack Hayhurst <jhayhurst@liquidweb.com> 
- Wrote inital build script and changelog.
