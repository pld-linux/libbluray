#
# TODO:
#  Build with bdjava (0.2.1 tarball doesn't have all necessary files)
#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
Summary:	Library to access Blu-Ray disks for video playback
Summary(pl.UTF-8):	Biblioteka dostępu do dysków Blu-Ray w celu odtwarzania filmów
Name:		libbluray
Version:	0.2.1
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	ftp://ftp.videolan.org/pub/videolan/libbluray/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	d4cfcf3f110e9d2afe01d29feb8c842b
URL:		http://www.videolan.org/developers/libbluray.html
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	doxygen
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 1:2.6.0
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package is aiming to provide a full portable free open source
bluray library, which can be plugged into popular media players to
allow full bluray navigation and playback on Linux. It will eventually
be compatible with all current titles, and will be easily portable and
embeddable in standard players such as mplayer and vlc.

%description -l pl
Ten pakiet ma w zamierzeniu dostarczać w pełni przenośną,
wolnodostępną i mającą otwarte źródła biblioteką bluray, dającą się
wykorzystać w popularnych odtwarzaczach multimedialnych w celu
pełnej nawigacji i odtwarzania filmów pod Linuksem. Ostatecznie
powinna być kompatybilna ze wszystkimi bieżącymi tytułami, łatwo
przenośna i dająca się wbudować w standardowe odtwarzacze, takie jak
mplayer czy vlc.

%package devel
Summary:	Header files for libbluray library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libbluray
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libbluray library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libbluray.

%package static
Summary:	Static libbluray library
Summary(pl.UTF-8):	Statyczna biblioteka libbluray
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libbluray library.

%description static -l pl.UTF-8
Statyczna biblioteka libbluray.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{__enable_disable static_libs static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.txt
%attr(755,root,root) %{_libdir}/libbluray.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libbluray.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbluray.so
%{_includedir}/libbluray
%{_pkgconfigdir}/libbluray.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libbluray.a
%endif
