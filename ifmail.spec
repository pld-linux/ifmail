# TODO: standardize %pre

%define txver 8.10

Summary:	FIDO <=> INTERNET Gateway
Summary(pl.UTF-8):	Bramka FIDO <=> INTERNET
Name:		ifmail
Version:	2.14tx%{txver}
Release:	0.1
Epoch:		1
License:	GPL
Group:		Networking
Source0:	http://ftp.debian.org/debian/pool/main/i/ifmail/%{name}_%{version}.orig.tar.gz
# Source0-md5:	2e1563ff2f370dfa95d23b8331a3a0eb
Source1:	%{name}-config
Source2:	%{name}-Areas
# from:	http://ftp.debian.org/debian/pool/main/i/ifmail/ifmail_%{version}-18.diff.gz
Patch0:		%{name}-debian.patch
Patch1:		%{name}-ndbm.patch
Patch2:		%{name}-install.patch
URL:		http://www.average.org/ifmail/
BuildRequires:	flex
BuildRequires:	gdbm-devel
BuildRequires:	mawk
BuildRequires:	rpmbuild(macros) >= 1.202
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/useradd
Provides:	user(ifmail)
Obsoletes:	ifmail
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
FIDO <=> INTERNET Gateway.

%description -l pl.UTF-8
Bramka FIDO <=> INTERNET.

%prep
%setup -q -n %{name}-%{version}.orig
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir}/%{name},%{_sysconfdir}/%{name},/var/log/%{name}}
install -d $RPM_BUILD_ROOT/var/spool/%{name}/{inb,outb}
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/maptabs

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install misc/maptabs/*	$RPM_BUILD_ROOT%{_datadir}/%{name}/maptabs/
install %{SOURCE1}	$RPM_BUILD_ROOT%{_sysconfdir}/%{name}/config
install %{SOURCE2}	$RPM_BUILD_ROOT%{_sysconfdir}/%{name}/Areas

touch $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/passwd
touch $RPM_BUILD_ROOT/var/log/%{name}/ifmail
touch $RPM_BUILD_ROOT/var/log/%{name}/ifdebug

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%useradd -g uucp -d /usr/lib/ifmail -u 110 -s /bin/true ifmail

%postun
if [ "$1" = "0" ]; then
	%userremove ifmail
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc ifcico/{README.mxlookup,hydra.LICENSE.DOC}
%doc misc/{FAQ,README,DEBUG}
%doc md/{ifmail.m4,fidosend,ifpoll,mailertable,newsfeeds,fido.daily}
%attr(4755,ifmail,uucp) %{_libexecdir}/%{name}/* # FIXME no globs for suid/sgid files
%attr(644,ifmail,uucp) %config %{_sysconfdir}/%{name}/config
%attr(644,ifmail,uucp) %config %{_sysconfdir}/%{name}/Areas
%attr(644,ifmail,uucp) %config %{_sysconfdir}/%{name}/passwd
%attr(755,ifmail,uucp) %dir %{_datadir}/%{name}
%attr(755,ifmail,uucp) %dir %{_datadir}/%{name}/maptabs/
%attr(644,ifmail,uucp) %{_datadir}/%{name}/maptabs/*
%attr(755,ifmail,uucp) %dir /var/spool/%{name}
%attr(755,ifmail,uucp) %dir /var/spool/%{name}/inb
%attr(755,ifmail,uucp) %dir /var/spool/%{name}/outb
%attr(755,ifmail,uucp) %dir /var/log/%{name}
%attr(644,ifmail,uucp) %ghost /var/log/%{name}/ifmail
%attr(644,ifmail,uucp) %ghost /var/log/%{name}/ifdebug
