%global log_dir var/log/loadwatch
%global legacy_log_dir root/loadwatch
%global conf etc/default/%{name}
%global bin usr/local/lp/bin/%{name}
%global cron etc/cron.d/%{name}.cron
Summary: A script to monitor a system for abnormal conditions, and log data
Name: loadwatch
Version: 1.2.2
Release: 0
URL: https://github.com/jakdept/loadwatch
License: MIT
Group: Applications/System
Packager: Jack Hayhurst <support-tools@liquidweb.com>
BuildRoot: %{_topdir}/%{name}
BuildArch: noarch
Requires: bash, cronie, lynx, sed, /bin/find

%description
The loadwatch script runs on an interval, and monitors the system for errant
conditions - high load, high swap usage, high httpd or MySQL utilization.

When errant conditions are detected, certain information is dumped to a file
for later inspection.

%prep

%build

%install
mkdir -p \
  %{buildroot}/usr/local/lp/bin \
  %{buildroot}/etc/default \
  %{buildroot}/etc/cron.d \
  %{buildroot}/root \
  %{buildroot}/%{log_dir}
echo %{buildroot}
echo %{_sourcedir}/%{name}
ln -s -f -L /%{log_dir} %{buildroot}/%{legacy_log_dir}
install -m 0700 %{_sourcedir}/%{name}/loadwatch %{buildroot}/%{bin}
install -m 755 %{_sourcedir}/%{name}/loadwatch.env %{buildroot}/%{conf}
install -m 0600 %{_sourcedir}/%{name}/loadwatch.cron %{buildroot}/%{cron}
touch %{buildroot}/etc/plbakeloadwatchinstalled

%pre
[[ -d /%{log_dir} ]] && mkdir -p /%{log_dir}
[[ -f /%{legacy_log_dir}/checklog ]] && mv /%{legacy_log_dir}/checklog /%{log_dir}/check.log
[[ -f /var/log/loadwatch.log ]] && mv /var/log/loadwatch.log /%{log_dir}/check.log
if [[ -d /%{legacy_log_dir} ]]; then
  rsync -aHl /%{legacy_log_dir}/ /%{log_dir}/ >/dev/null
  rm -rf /root/loadwatch
fi
rm -f /root/bin/loadwatch.sh /root/bin/loadwatch
sed -i -e '/\/root\/bin\/loadwatch/d' -e '/\/root\/loadwatch/d' /var/spool/cron/root

%post
# with next version uncomment the following line
# if [[ $1 -eq '1' ]]; then
  # disable apache statistics if not on cPanel - they can manually be enabled later
  if [[ -f /usr/local/cpanel/version ]]; then
    sed -i -e '/^APACHEURI/d' -e '/^APACHEPORT/d' /%{conf}

    port=$(netstat -tpln | \
      awk '$7 ~ /httpd$/ && $4 ~/[[:digit:]]:.*0$/ {gsub("^.*:", "", $4); print $4}')

    echo "APACHEURI='/whm-server-status'" >> /%{conf}
    echo "APACHEPORT=${port}" >> /%{conf}
  fi
# with the next version, uncomment the next line
# fi

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)

%dir /%{log_dir}
%config(noreplace) /%{conf}
/%{bin}
/%{cron}
/%{legacy_log_dir}
/etc/plbakeloadwatchinstalled

%changelog
* Thu Aug 08 2019 Jack Hayhurst <jhayhurst@liquidweb.com> 1.2.2
- fixes a typo
- setup CI automation for build

* Mon Jul 16 2018 Jack Hayhurst <jhayhurst@liquidweb.com> 1.2.1
- fixes a typo

* Tue May 01 2018 Jack Hayhurst <jhayhurst@liquidweb.com> 1.2.0
- changed default action to add support for platforms other than cPanel
- Plesk is now supported
- added support for alternate Apache Status URI's
- fixed /var/log/loadwatc/loadwatch bug

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
