Summary:	FIDO <=> INTERNET Gateway
Summary(pl):	Bramka FIDO <=> INTERNET
Name:		ifmail
Version:	2.15
Release:	1
License:	GPL
Group:		Networking
Group(de):	Netzwerkwesen
Group(pl):	Sieciowe
Source0:	%{name}-%{version}.tar.gz
Source1:	%{name}-config
Source2:	%{name}-Areas
Patch0:		%{name}-makefile.patch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Buildrequires:	bison

%description
FIDO <=> INTERNET Gateway.

%prep
%setup -q
%patch -p1

%build
%{__make} CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir}/%{name},%{_sysconfdir}/%{name},/var/log/%{name}}
install -d $RPM_BUILD_ROOT/var/spool/%{name}/{inb,outb}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install misc/inouttabs/*	$RPM_BUILD_ROOT%{_libdir}/%{name}
install misc/getnodelist	$RPM_BUILD_ROOT%{_libdir}/%{name}
install %{SOURCE1}	$RPM_BUILD_ROOT%{_sysconfdir}/%{name}/config
install %{SOURCE2}	$RPM_BUILD_ROOT%{_sysconfdir}/%{name}/Areas

touch $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/passwd
touch $RPM_BUILD_ROOT/var/log/%{name}/ifmail
touch $RPM_BUILD_ROOT/var/log/%{name}/ifdebug

gzip -9nf misc/{FAQ,README}

%pre
UID=63; GROUP=uucp; HOMEDIR=/usr/lib/ifmail; %useradd

%postun
%userdel

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc misc/{FAQ,README}.gz

%attr(4755,ifmail,uucp) %{_libdir}/%{name}/ifcico
%attr(4755,ifmail,uucp) %{_libdir}/%{name}/ifindex
%attr(4755,ifmail,uucp) %{_libdir}/%{name}/nlpatch
%attr(4755,ifmail,uucp) %{_libdir}/%{name}/ifstat
%attr(4755,ifmail,uucp) %{_libdir}/%{name}/ifmail

%attr(755,ifmail,uucp) %{_libdir}/%{name}/ifpack
%attr(755,ifmail,uucp) %{_libdir}/%{name}/ifunpack
%attr(755,ifmail,uucp) %{_libdir}/%{name}/iftoss

%attr(755,ifmail,uucp) %{_libdir}/%{name}/getnodelist

%attr(644,ifmail,uucp) %{_libdir}/%{name}/cp895__cp437
%attr(644,ifmail,uucp) %{_libdir}/%{name}/cp895__iso-8859-2
%attr(644,ifmail,uucp) %{_libdir}/%{name}/fidom2iso
%attr(644,ifmail,uucp) %{_libdir}/%{name}/fidomazovia
%attr(644,ifmail,uucp) %{_libdir}/%{name}/ibmpc-latin1
%attr(644,ifmail,uucp) %{_libdir}/%{name}/iso-8859-2__cp895
%attr(644,ifmail,uucp) %{_libdir}/%{name}/iso2fidom
%attr(644,ifmail,uucp) %{_libdir}/%{name}/latin1-ibmpc
%attr(644,ifmail,uucp) %{_libdir}/%{name}/outaltkoi8
%attr(644,ifmail,uucp) %{_libdir}/%{name}/outkoi8alt

%attr(644,ifmail,uucp) %{_sysconfdir}/%{name}/config
%attr(644,ifmail,uucp) %{_sysconfdir}/%{name}/Areas

%attr(644,ifmail,uucp) %ghost %{_sysconfdir}/%{name}/passwd

%attr(755,ifmail,uucp) %dir /var/spool/%{name}
%attr(755,ifmail,uucp) %dir /var/log/%{name}

%attr(644,ifmail,uucp) %ghost /var/log/%{name}/ifmail
%attr(644,ifmail,uucp) %ghost /var/log/%{name}/ifdebug
