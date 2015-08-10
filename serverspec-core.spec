%global install_dir /opt/gdc/serverspec-core

Name:             serverspec-core
Summary:          GoodData ServerSpec integration
Version:          1.5
Release:          1.gdc

Vendor:           GoodData
Group:            GoodData/Tools

License:          Gooddata proprietary
URL:              https://github.com/gooddata/serverspec-core
Source0:          sources.tar
BuildArch:        x86_64
BuildRoot:        %{_tmppath}/%{name}-%{version}-root

Requires:         ruby193-rubygem-bundler

%prep
%setup -q -c

%install
rm -fr $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{install_dir}
cp -a * .bundle $RPM_BUILD_ROOT%{install_dir}
install -d $RPM_BUILD_ROOT/usr/bin
mv ./bin/serverspec $RPM_BUILD_ROOT/usr/bin/serverspec
install -d $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/
mv $RPM_BUILD_ROOT%{install_dir}/serverspec.sysconfig $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/serverspec

%clean
rm -rf $RPM_BUILD_ROOT

%description
GoodData ServerSpec integration - core package

%files
%attr(0755, root, root) %dir %{install_dir}
%attr(0755, root, root) %{install_dir}/.bundle
%attr(0755, root, root) %{install_dir}/bundle
%attr(0755, root, root) %{install_dir}/bin
%attr(0755, root, root) %dir %{install_dir}/cfg
%attr(0755, root, root) %dir %{install_dir}/spec
%attr(0755, root, root) %dir %{install_dir}/reports
%attr(0755, root, root) %{install_dir}/spec/types
%attr(0755, root, root) %{install_dir}/cfg/cfg_helper.rb
%attr(0755, root, root) %{install_dir}/cfg/serverspec.yml
%attr(0755, root, root) %{install_dir}/cfg/local.yml
%attr(0755, root, root) %{install_dir}/check_last_run.sh
%attr(0755, root, root) %{install_dir}/cron_run.sh
%attr(0755, root, root) %{install_dir}/Gemfile*
%attr(0755, root, root) %{install_dir}/Rakefile
%attr(0755, root, root) %{install_dir}/serverspec-core.spec
%attr(0755, root, root) %{install_dir}/spec/spec_helper.rb
%attr(0755, root, root) %{install_dir}/spec/common/test/hosts_spec.rb
%attr(0755, root, root) %doc %{install_dir}/*.md
%attr(0644, root, root) %config(noreplace) %{_sysconfdir}/sysconfig/serverspec
%attr(0755, root, root) /usr/bin/serverspec
%exclude %{install_dir}/Makefile
%exclude %{install_dir}/makemeusable
%exclude %{install_dir}/bundle.log
%exclude %{install_dir}/reports/.gitignore
%exclude %{install_dir}/spec/types/.gitignore

%changelog
* Mon Aug 10 2015 Martin Surovcak <martin.surovcak@gooddata.com> 1.5-1.gdc
- Add cista related gems

* Mon Aug 10 2015 Yury Tsarev <yury.tsarev@gooddata.com> 1.4-1.gdc
- Add junit formatter

* Mon Aug 10 2015 Yury Tsarev <yury.tsarev@gooddata.com> 1.3-5.gdc
- Fix the case of undefined roles for host

* Wed Aug 05 2015 Yury Tsarev <yury.tsarev@gooddata.com> 1.3-4.gdc
- Compile overall json report also with default rake task

* Wed Aug 05 2015 Yury Tsarev <yury.tsarev@gooddata.com> 1.3-3.gdc
- Add runtime dependency on bundler

* Tue Aug 04 2015 Yury Tsarev <yury.tsarev@gooddata.com> 1.3-2.gdc
- Update cron_run.sh to use bundled serverspec

* Tue Aug 04 2015 Yury Tsarev <yury.tsarev@gooddata.com> 1.3-1.gdc
- Update dependencies in bundle to include recent specinfra enhancements
- Provide default rake task so the user can just run `serverspec` for testing

* Tue Aug 04 2015 Yury Tsarev <yury.tsarev@gooddata.com> 1.2-2.gdc
- Package serverspec together with isolated rubygem bundle
- Introduce systemwide wrapper of /usr/bin/serverspec

* Mon Jul 20 2015 Martin Surovcak <martin.surovcak@gooddata.com> 1.1-2.gdc
- fix _spec.rb inclusion in SPEC_DIR

* Thu Jul 16 2015 Yury Tsarev <yury.tsarev@gooddata.com> 1.1-1.gdc
- Sample minimal local configuration provided
- Output formatting option in CLI
- Tag filtering ability in CLI

* Tue Jul 14 2015 Martin Surovcak <martin.surovcak@gooddata.com> 1.0-11.gdc
- fixed bug when including custom types

* Mon Jul 13 2015 Martin Surovcak <martin.surovcak@gooddata.com> 1.0-10.gdc
- types are included from both SPEC_DIR and pgk_root paths
- fix YAML include
- get_all_hosts respects CFG_DIR option

* Thu Jul 02 2015 Martin Surovcak <martin.surovcak@gooddata.com> 1.0-9.gdc
- default spec_helper provides SPEC_DIR to all included specs and helpers
- spec/types is back

* Thu Jul 02 2015 Martin Surovcak <martin.surovcak@gooddata.com> 1.0-8.gdc
- exclude reports/.gitignore

* Thu Jul 02 2015 Martin Surovcak <martin.surovcak@gooddata.com> 1.0-7.gdc
- create default reports directory while installing package
- do not include types in package - they should be delivered with specs

* Wed Jul 01 2015 Martin Surovcak <martin.surovcak@gooddata.com> 1.0-6.gdc
- cron should not exec bundle anymore

* Mon Jun 29 2015 Radek Smidl <radek.smidl@gooddata.com> 1.0-5.gdc
- REPORTS_PATH renamed to REPORTS_DIR

* Mon Jun 29 2015 Radek Smidl <radek.smidl@gooddata.com> 1.0-4.gdc
- CONF_DIR and SPEC_DIR options added

* Mon Jun 29 2015 Radek Smidl <radek.smidl@gooddata.com> 1.0-3.gdc
- sysconfig support added

* Wed Jun 10 2015 Yury Tsarev <yury.tsarev@gooddata.com> 1.0-2.gdc
- Fix versioning and file inclusion

* Tue Jun 09 2015 Martin Surovcak <martin.surovcak@gooddata.com> 1.0-1.gdc
- Initial rpmbuild