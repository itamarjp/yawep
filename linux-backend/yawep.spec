Name:           yawep
Version:        0.0.0
Release:        1%{?dist}
Summary:        Yet Another Web Hosting Control Panel


License:        GPLv2+
URL:            https://github.com/itamarjp/yawep
Source0:        yawep.tar.gz

#BuildRequires:  php
Requires:       httpd

%description
Yet Another Web Hosting Control Panel

%prep
%autosetup


%build
# % configure
# % make_build


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
# make _install
touch $RPM_BUILD_ROOT/%{_sysconfdir}/dovecot/local.conf

%files
# % license 
%doc linux-backend/readme.txt
%config(noreplace) %{_sysconfdir}/dovecot/local.conf


%changelog
* Sun Feb  4 2018 itamar <itamar@ispbrasil.com.br>
- 
