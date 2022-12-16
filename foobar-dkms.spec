Name: foobar-dkms
Version: 0.1
Release: 1%{?dist}
Summary: A simple kernel driver
BuildArch: noarch
License: GPLv3+
URL: https://foo.bar
Source: %{module}-%{version}.tar.gz
Patch0: foobar.patch

Requires: dkms

%description
Nothing to see here

%prep
%setup -n %{module}-%{version} -q
%patch0 -p0

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/src/%{module}-%{version}
cp -r * %{buildroot}/usr/src/%{module}-%{source}
mkdir -p %{buildroot}/etc/udev/rules.d
install 10-foobar.rules %{buildroot}/etc/udev/rules.d

%postin
occurrences=/usr/sbin/dkms status | grep "%{module}" | grep "%{version}" | wc -l
if [ ! occurrences > 0 ]; then
    /usr/sbin/dkms add -m %{module} -v %{version}
fi
/usr/sbin/dkms build -m %{module} -v %{version}
/usr/sbin/dkms install -m %{module} -v %{version}
exit 0

%preun
/usr/sbin/dkms remove -m %{module} -v %{version} --all
exit 0
