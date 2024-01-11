# Enable python3
%bcond_without python3

# Disable python2
%bcond_with python2

# RHEL8: Tests disabled due to missing deps
%bcond_with tests

%global srcname cryptography

Name:           python-%{srcname}
Version:        3.3.1
Release:        2%{?dist}
Summary:        PyCA's cryptography library

License:        ASL 2.0 or BSD
URL:            https://cryptography.io/en/latest/
Source0:        %{pypi_source}
Source1:        %{pypi_source}.asc
# key ids of upstream authors are published in the AUTHORS file:
#    https://github.com/pyca/cryptography/blob/master/AUTHORS.rst
# gpg2 --recv-keys "05FD 9FA1 6CF7 5735 0D91 A560 235A E5F1 29F9 ED98"
# gpg2 --export --export-options export-minimal "05FD 9FA1 6CF7 5735 0D91 A560 235A E5F1 29F9 ED98" > gpgkey-05FD_9FA1_6CF7_5735_0D91_A560_235A_E5F1_29F9_ED98.gpg
Source2:        gpgkey-05FD_9FA1_6CF7_5735_0D91_A560_235A_E5F1_29F9_ED98.gpg

# Exclude i686 arch. Due to a modularity issue it's being added to the
# x86_64 compose of CRB, but we don't want to ship it at all.
# See: https://projects.engineering.redhat.com/browse/RCM-72605
ExcludeArch: i686

BuildRequires:  openssl-devel
BuildRequires:  gcc
BuildRequires:  gnupg2

%if 0%{?with_python2}
BuildRequires:  python2-cffi >= 1.7
BuildRequires:  python2-cryptography-vectors = %{version}
BuildRequires:  python2-devel
BuildRequires:  python2-enum34
BuildRequires:  python2-idna >= 2.1
BuildRequires:  python2-ipaddress
BuildRequires:  python2-setuptools
BuildRequires:  python2-six >= 1.4.1

%if %{with tests}
BuildRequires:  python2-hypothesis >= 1.11.4
BuildRequires:  python2-iso8601
BuildRequires:  python2-pretend
BuildRequires:  python2-pytest >= 3.2.1
BuildRequires:  python2-pytz
%endif
%endif

%if 0%{?with_python3}
BuildRequires:  python%{python3_pkgversion}-cffi >= 1.7
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-rpm-macros
BuildRequires:  python%{python3_pkgversion}-idna >= 2.1
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-six >= 1.4.1

%if %{with tests}
BuildRequires:  python%{python3_pkgversion}-cryptography-vectors = %{version}
BuildRequires:  python%{python3_pkgversion}-hypothesis >= 1.11.4
BuildRequires:  python%{python3_pkgversion}-iso8601
BuildRequires:  python%{python3_pkgversion}-pretend
BuildRequires:  python%{python3_pkgversion}-pytest >= 3.2.1
BuildRequires:  python%{python3_pkgversion}-pytz
%endif
%endif

%description
cryptography is a package designed to expose cryptographic primitives and
recipes to Python developers.

%if 0%{?with_python2}
%package -n  python2-%{srcname}
Summary:        PyCA's cryptography library

%if 0%{?with_python3}
%{?python_provide:%python_provide python2-%{srcname}}
%else
Provides:       python-%{srcname}
%endif

Requires:       openssl-libs
Requires:       python2-idna >= 2.1
Requires:       python2-six >= 1.4.1
Requires:       python2-cffi >= 1.7
Requires:       python2-enum34
Requires:       python2-ipaddress

%description -n python2-%{srcname}
cryptography is a package designed to expose cryptographic primitives and
recipes to Python developers.
%endif

%if 0%{?with_python3}
%package -n  python%{python3_pkgversion}-%{srcname}
Summary:        PyCA's cryptography library
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}

Requires:       openssl-libs
Requires:       python%{python3_pkgversion}-idna >= 2.1
Requires:       python%{python3_pkgversion}-six >= 1.4.1
Requires:       python%{python3_pkgversion}-cffi >= 1.7

%description -n python%{python3_pkgversion}-%{srcname}
cryptography is a package designed to expose cryptographic primitives and
recipes to Python developers.
%endif

%prep
# RHEL8: GPGverify macro is not present in RHEL
# %%{gpgverify} --keyring='%%{SOURCE2}' --signature='%%{SOURCE1}' --data='%%{SOURCE0}'
%autosetup -p1 -n %{srcname}-%{version}

%build
%if 0%{?with_python2}
%py2_build
%endif
%if 0%{?with_python3}
%py3_build
%endif

%install
# Actually other *.c and *.h are appropriate
# see https://github.com/pyca/cryptography/issues/1463
find . -name .keep -print -delete

%if 0%{?with_python2}
%py2_install
%endif
%if 0%{?with_python3}
%py3_install
%endif

%check
%if %{with tests}
%if 0%{?with_python2}
# see https://github.com/pyca/cryptography/issues/4885 and
# see https://bugzilla.redhat.com/show_bug.cgi?id=1761194 for deselected tests
PYTHONPATH=%{buildroot}%{python2_sitearch} %{__python2} -m pytest -k "not (test_buffer_protocol_alternate_modes or test_dh_parameters_supported or test_load_ecdsa_no_named_curve)"
%endif

%if 0%{?with_python3}
PYTHONPATH=%{buildroot}%{python3_sitearch} %{__python3} -m pytest -k "not (test_buffer_protocol_alternate_modes or test_dh_parameters_supported or test_load_ecdsa_no_named_curve)"
%endif
%endif


%if 0%{?with_python2}
%files -n python2-%{srcname}
%doc LICENSE LICENSE.APACHE LICENSE.BSD README.rst docs
%{python2_sitearch}/%{srcname}
%{python2_sitearch}/%{srcname}-%{version}-py*.egg-info
%endif


%if 0%{?with_python3}
%files -n python%{python3_pkgversion}-%{srcname}
%doc README.rst docs
%license LICENSE LICENSE.APACHE LICENSE.BSD
%{python3_sitearch}/%{srcname}
%{python3_sitearch}/%{srcname}-%{version}-py*.egg-info
%endif


%changelog
* Mon Jan 18 2021 Tomas Orsava <torsava@redhat.com> - 3.3.1-2
- Convert from Fedora to the python39 module in RHEL8
- Resolves: rhbz#1877430

* Thu Dec 10 2020 Christian Heimes <cheimes@redhat.com> - 3.3.1-1
- Update to 3.3.1 (#1905756)

* Wed Oct 28 2020 Christian Heimes <cheimes@redhat.com> - 3.2.1-1
- Update to 3.2.1 (#1892153)

* Mon Oct 26 2020 Christian Heimes <cheimes@redhat.com> - 3.2-1
- Update to 3.2 (#1891378)

* Mon Sep 07 2020 Christian Heimes <cheimes@redhat.com> - 3.1-1
- Update to 3.1 (#1872978)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 21 2020 Christian Heimes <cheimes@redhat.com> - 3.0-1
- Update to 3.0 (#185897)

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 2.9-3
- Rebuilt for Python 3.9

* Tue May 12 2020 Felix Schwarz <fschwarz@fedoraproject.org> - 2.9-2
- add source file verification

* Fri Apr 03 2020 Christian Heimes <cheimes@redhat.com> - 2.9-1
- Update to 2.9 (#1820348)

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 13 2020 Christian Heimes <cheimes@redhat.com> - 2.8-2
- cryptography 2.8+ no longer depends on python-asn1crypto

* Thu Oct 17 2019 Christian Heimes <cheimes@redhat.com> - 2.8-1
- Update to 2.8
- Resolves: rhbz#1762779

* Sun Oct 13 2019 Christian Heimes <cheimes@redhat.com> - 2.7-3
- Skip unit tests that fail with OpenSSL 1.1.1.d
- Resolves: rhbz#1761194
- Fix and simplify Python 3 packaging

* Sat Oct 12 2019 Christian Heimes <cheimes@redhat.com> - 2.7-2
- Drop Python 2 package
- Resolves: rhbz#1761081

* Tue Sep 03 2019 Randy Barlow <bowlofeggs@fedoraproject.org> - 2.7-1
- Update to 2.7 (#1715680).

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 2.6.1-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Feb 28 2019 Christian Heimes <cheimes@redhat.com> - 2.6.1-1
- New upstream release 2.6.1, resolves RHBZ#1683691

* Wed Feb 13 2019 Alfredo Moralejo <amoralej@redhat.com> - 2.5-1
- Updated to 2.5.

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Aug 13 2018 Christian Heimes <cheimes@redhat.com> - 2.3-2
- Use TLSv1.2 in test as workaround for RHBZ#1615143

* Wed Jul 18 2018 Christian Heimes <cheimes@redhat.com> - 2.3-1
- New upstream release 2.3
- Fix AEAD tag truncation bug, RHBZ#1602752

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 15 2018 Miro Hrončok <mhroncok@redhat.com> - 2.2.1-2
- Rebuilt for Python 3.7

* Wed Mar 21 2018 Christian Heimes <cheimes@redhat.com> - 2.2.1-1
- New upstream release 2.2.1

* Sun Feb 18 2018 Christian Heimes <cheimes@redhat.com> - 2.1.4-1
- New upstream release 2.1.4

* Sun Feb 18 2018 Christian Heimes <cheimes@redhat.com> - 2.1.3-4
- Build requires gcc

* Mon Feb 12 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.1.3-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild
