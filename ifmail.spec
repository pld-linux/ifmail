# TODO: standardize %pre
Summary:	FIDO <=> INTERNET Gateway
Summary(pl):	Bramka FIDO <=> INTERNET
Name:		ifmail
Version:	3.03
Release:	0.2
License:	GPL
Group:		Networking
Source0:	http://dl.sourceforge.net/ifmail/%{name}-%{version}.tar.gz
Source1:	%{name}-config
Source2:	%{name}-Areas
URL:		http://www.average.org/ifmail/
BuildRequires:	flex
BuildRequires:  gdbm-devel
BuildRequires:  mawk
Requires(pre):	/usr/sbin/useradd
Requires(postun):	/usr/sbin/userdel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
	
%description
FIDO <=> INTERNET Gateway.

%description -l pl
Bramka FIDO <=> INTERNET.

%prep
%setup -q

%build
%configure2_13 --libexecdir=%{_libexecdir}/%{name}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir}/%{name},%{_sysconfdir}/%{name},/var/log/%{name}}
install -d $RPM_BUILD_ROOT/var/spool/%{name}/{inb,outb}
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install misc/inouttabs/*	$RPM_BUILD_ROOT%{_datadir}/%{name}/
install %{SOURCE1}	$RPM_BUILD_ROOT%{_sysconfdir}/%{name}/config
install %{SOURCE2}	$RPM_BUILD_ROOT%{_sysconfdir}/%{name}/Areas

touch $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/passwd
touch $RPM_BUILD_ROOT/var/log/%{name}/ifmail
touch $RPM_BUILD_ROOT/var/log/%{name}/ifdebug

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ "$1" = "1" ]; then
	%{_sbindir}/useradd -g uucp -d /usr/lib/ifmail -u 63 -s /bin/true ifmail 2> /dev/null
fi

%postun
if [ "$1" = "0" ]; then
	%{_sbindir}/userdel ifmail 2> /dev/null
fi

%files
%defattr(644,root,root,755)
%doc misc/{FAQ,README,DEBUG}
%attr(4755,ifmail,uucp) %{_bindir}/ifstat
%attr(4755,ifmail,uucp) %{_libexecdir}/%{name}/*
%attr(644,ifmail,uucp) %{_datadir}/%{name}/*
%attr(644,ifmail,uucp) %{_sysconfdir}/%{name}/config
%attr(644,ifmail,uucp) %{_sysconfdir}/%{name}/Areas
%attr(644,ifmail,uucp) %ghost %{_sysconfdir}/%{name}/passwd
%attr(755,ifmail,uucp) %dir /var/spool/%{name}
%attr(755,ifmail,uucp) %dir /var/spool/%{name}/inb
%attr(755,ifmail,uucp) %dir /var/spool/%{name}/outb
%attr(755,ifmail,uucp) %dir /var/log/%{name}
%attr(644,ifmail,uucp) %ghost /var/log/%{name}/ifmail
%attr(644,ifmail,uucp) %ghost /var/log/%{name}/ifdebug
