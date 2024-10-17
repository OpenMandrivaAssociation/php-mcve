%define modname mcve
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A44_%{modname}.ini

Summary:	libmonetra/libmcve interface for php
Name:		php-%{modname}
Version:	7.0.3
Release:	14
Group:		Development/PHP
License:	PHP License
URL:		https://pecl.php.net/package/mcve
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
Source1:	%{modname}.ini
Patch0:		mcve-7.0.3-php54x.diff
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	libmonetra-devel >= 7.0.0
BuildRequires:	openssl-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Interface the MCVE/Monetra API (libmonetra [formerly libmcve]), allowing you to
work directly with MCVE/Monetra from your PHP scripts. Monetra is Main Street
Softworks' solution to direct credit card processing for Unix.

%prep

%setup -q -n %{modname}-%{version}
[ "../package*.xml" != "/" ] && mv ../package*.xml .

%patch0 -p0

cp %{SOURCE1} %{inifile}

# fix version
perl -pi -e "s|#define PHP_MCVE_VERSION \"7\.0\.2\"|#define PHP_MCVE_VERSION \"%{version}\"|g" php_mcve.h

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --enable-%{modname}=shared,%{_prefix} \
    --with-openssl-dir=%{_prefix}

%make
#make test
mv modules/*.so .

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m0755 %{soname} %{buildroot}%{_libdir}/php/extensions/
install -m0644 %{inifile} %{buildroot}%{_sysconfdir}/php.d/%{inifile}

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc package*.xml CREDITS tests *.php
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}


%changelog
* Sun May 06 2012 Oden Eriksson <oeriksson@mandriva.com> 7.0.3-13mdv2012.0
+ Revision: 797076
- fix build
- rebuild for php-5.4.x

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 7.0.3-12
+ Revision: 761265
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 7.0.3-11
+ Revision: 696441
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 7.0.3-10
+ Revision: 695419
- rebuilt for php-5.3.7

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 7.0.3-9
+ Revision: 646658
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 7.0.3-8mdv2011.0
+ Revision: 629823
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 7.0.3-7mdv2011.0
+ Revision: 628147
- ensure it's built without automake1.7

* Wed Nov 24 2010 Oden Eriksson <oeriksson@mandriva.com> 7.0.3-6mdv2011.0
+ Revision: 600505
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 7.0.3-5mdv2011.0
+ Revision: 588843
- rebuild

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 7.0.3-4mdv2010.1
+ Revision: 514571
- rebuilt for php-5.3.2

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 7.0.3-3mdv2010.1
+ Revision: 485402
- rebuilt for php-5.3.2RC1

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 7.0.3-2mdv2010.1
+ Revision: 468185
- rebuilt against php-5.3.1

* Sat Oct 03 2009 Oden Eriksson <oeriksson@mandriva.com> 7.0.3-1mdv2010.0
+ Revision: 452826
- 7.0.3
- the php531 fix was fixed upstream (P0)

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 7.0.2-3mdv2010.0
+ Revision: 451504
- fix build
- rebuild
- 7.0.2
- rebuilt for php-5.3.0RC2

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

  + Raphaël Gertz <rapsys@mandriva.org>
    - Rebuild

* Sun Mar 01 2009 Oden Eriksson <oeriksson@mandriva.com> 7.0.1-6mdv2009.1
+ Revision: 346516
- rebuilt for php-5.2.9

* Tue Feb 17 2009 Oden Eriksson <oeriksson@mandriva.com> 7.0.1-5mdv2009.1
+ Revision: 341775
- rebuilt against php-5.2.9RC2

* Sun Jan 04 2009 Oden Eriksson <oeriksson@mandriva.com> 7.0.1-4mdv2009.1
+ Revision: 324312
- rebuild

* Fri Dec 05 2008 Oden Eriksson <oeriksson@mandriva.com> 7.0.1-3mdv2009.1
+ Revision: 310285
- rebuilt against php-5.2.7

* Fri Jul 18 2008 Oden Eriksson <oeriksson@mandriva.com> 7.0.1-2mdv2009.0
+ Revision: 238410
- rebuild

* Mon May 12 2008 Oden Eriksson <oeriksson@mandriva.com> 7.0.1-1mdv2009.0
+ Revision: 206280
- 7.0.1

* Tue May 06 2008 Oden Eriksson <oeriksson@mandriva.com> 7.0.0-1mdv2009.0
+ Revision: 201823
- 7.0.0

* Fri May 02 2008 Oden Eriksson <oeriksson@mandriva.com> 5.2.2-9mdv2009.0
+ Revision: 200248
- rebuilt for php-5.2.6

* Mon Feb 04 2008 Oden Eriksson <oeriksson@mandriva.com> 5.2.2-8mdv2008.1
+ Revision: 162232
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Nov 11 2007 Oden Eriksson <oeriksson@mandriva.com> 5.2.2-7mdv2008.1
+ Revision: 107678
- restart apache if needed

* Sat Sep 01 2007 Oden Eriksson <oeriksson@mandriva.com> 5.2.2-6mdv2008.0
+ Revision: 77558
- rebuilt against php-5.2.4

* Thu Jun 14 2007 Oden Eriksson <oeriksson@mandriva.com> 5.2.2-5mdv2008.0
+ Revision: 39507
- use distro conditional -fstack-protector

* Fri Jun 01 2007 Oden Eriksson <oeriksson@mandriva.com> 5.2.2-4mdv2008.0
+ Revision: 33857
- rebuilt against new upstream version (5.2.3)

* Thu May 03 2007 Oden Eriksson <oeriksson@mandriva.com> 5.2.2-3mdv2008.0
+ Revision: 21340
- rebuilt against new upstream version (5.2.2)


* Thu Feb 08 2007 Oden Eriksson <oeriksson@mandriva.com> 5.2.2-2mdv2007.0
+ Revision: 117598
- rebuilt against new upstream version (5.2.1)

* Wed Feb 07 2007 Oden Eriksson <oeriksson@mandriva.com> 5.2.2-1mdv2007.1
+ Revision: 117295
- 5.2.2

* Thu Jan 11 2007 Oden Eriksson <oeriksson@mandriva.com> 5.2.1-1mdv2007.1
+ Revision: 107498
- 5.2.1

* Wed Nov 08 2006 Oden Eriksson <oeriksson@mandriva.com> 5.2.0-7mdv2007.1
+ Revision: 78212
- bunzip the ini file
- rebuilt for php-5.2.0
- Import php-mcve

* Mon Aug 28 2006 Oden Eriksson <oeriksson@mandriva.com> 5.2.0-5
- rebuilt for php-5.1.6

* Thu Jul 27 2006 Oden Eriksson <oeriksson@mandriva.com> 5.2.0-4mdk
- rebuild

* Sat May 06 2006 Oden Eriksson <oeriksson@mandriva.com> 5.2.0-3mdk
- rebuilt for php-5.1.4

* Sat May 06 2006 Oden Eriksson <oeriksson@mandriva.com> 5.2.0-2mdk
- rebuilt for php-5.1.3

* Sun Feb 05 2006 Oden Eriksson <oeriksson@mandriva.com> 5.2.0-1mdk
- initial Mandriva package

