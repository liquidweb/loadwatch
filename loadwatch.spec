Summary: A script to monitor a system for abnormal conditions, and log data
Name: loadwatch
Version: 1.1.0
Release: 0
URL: https://github.com/jakdept/loadwatch
License: MIT
Group: Applications/System
BuildRoot: %{_topdir}/%{name}-%{version}-%{release}-build
BuildArch: noarch
Requires: bash, cronie, lynx, sed, /bin/find

%description
The loadwatch script runs on an interval, and monitors the system for errant
conditions - high load, high swap usage, high httpd or MySQL utilization.

When errant conditions are detected, certain information is dumped to a file
for later inspection.

%prep
rm -rf ${RPM_BUILD_DIR}/loadwatch
curl -L https://github.com/jackknifed/loadwatch/archive/v%{version}.tar.gz | tar xz

%build

%install
mkdir -p \
  %{buildroot}/usr/local/lp/bin \
  %{buildroot}/etc/default \
  %{buildroot}/etc/cron.d \
  %{buildroot}/var/log/loadwatch
ln -s -f -L /var/log/loadwatch ${buildroot}/root/loadwatch
install -m 0700 ${RPM_BUILD_DIR}/loadwatch-%{version}/loadwatch %{buildroot}/usr/local/lp/bin/loadwatch
install -m 755 ${RPM_BUILD_DIR}/loadwatch-%{version}/loadwatch.env %{buildroot}/etc/default/loadwatch
install -m 0600 ${RPM_BUILD_DIR}/loadwatch-%{version}/loadwatch.cron %{buildroot}/etc/cron.d/loadwatch.cron
touch %{buildroot}/etc/plbakeloadwatchinstalled

%post
[[ -f /root/loadwatch/checklog ]] && mv /root/loadwatch/checklog /var/log/loadwatch/check.log
[[ -f /var/log/loadwatch.log ]] && mv /var/log/loadwatch.log /var/log/loadwatch/check.log
[[ -d /root/loadwatch ]] && rsync -aHl /root/loadwatch /var/log/loadwatch >/dev/null
rm -rf /root/loadwatch
rm -f /root/bin/loadwatch.sh /root/bin/loadwatch
sed -i -e '/\/root\/bin\/loadwatch/d' -e '/\/root\/loadwatch/d' /var/spool/cron/root


%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)

%dir /var/log/loadwatch
%config(noreplace) /etc/default/loadwatch
/usr/local/lp/bin/loadwatch
/etc/cron.d/loadwatch.cron
/root/loadwatch
/etc/plbakeloadwatchinstalled

%changelog
* Mon Oct 30 2017 Jack Hayhurst <jhayhurst@liquidweb.com> 1.1.0
- changed checklog name to /var/log/loadwatch/check.log
- changed output files to /var/log/loadwatch/date.txt
- changed mysql output format
- added symlink from /root/loadwatch to /var/log/loadwatch

* Wed Sep 06 2017 Jack Hayhurst <jhayhurst@liquidweb.com> 1.0.4
- adjusted cron so it works.
- added other minor changes requested.

* Mon Aug 28 2017 Jack Hayhurst <jhayhurst@liquidweb.com> 1.0.1
- reworked specfile, now installs

* Tue Nov 01 2016 Jack Hayhurst <jhayhurst@liquidweb.com> 
- Wrote inital build script and changelog.
