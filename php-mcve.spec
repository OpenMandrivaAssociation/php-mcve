%define modname mcve
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A44_%{modname}.ini

Summary:	libmonetra/libmcve interface for php
Name:		php-%{modname}
Version:	5.2.2
Release:	%mkrel 2
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/mcve
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tar.bz2
Source1:	%{modname}.ini
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	libmonetra-devel
BuildRequires:	openssl-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
Interface the MCVE/Monetra API (libmonetra [formerly libmcve]), allowing you to
work directly with MCVE/Monetra from your PHP scripts. Monetra is Main Street
Softworks' solution to direct credit card processing for Unix.

%prep

%setup -q -n %{modname}-%{version}
[ "../package*.xml" != "/" ] && mv ../package*.xml .

cp %{SOURCE1} %{inifile}

%build

phpize
%configure2_5x --with-libdir=%{_lib} \
    --enable-%{modname}=shared,%{_prefix} \
    --with-openssl-dir=%{_prefix}

%make
make test
mv modules/*.so .

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m0755 %{soname} %{buildroot}%{_libdir}/php/extensions/
install -m0644 %{inifile} %{buildroot}%{_sysconfdir}/php.d/%{inifile}

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc package*.xml CREDITS tests *.php
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}


