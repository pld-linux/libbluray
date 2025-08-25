#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	static_libs	# static library
%bcond_without	java		# BD-Java

%{?with_java:%{?use_default_jdk}}
Summary:	Library to access Blu-Ray disks for video playback
Summary(pl.UTF-8):	Biblioteka dostępu do dysków Blu-Ray w celu odtwarzania filmów
Name:		libbluray
Version:	1.4.0
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	https://download.videolan.org/videolan/libbluray/%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	13bda98cbb83cfb582f8a30c780da63d
URL:		http://www.videolan.org/developers/libbluray.html
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	fontconfig-devel
BuildRequires:	freetype-devel >= 2
BuildRequires:	libudfread-devel >= 1.2.0
BuildRequires:	libxml2-devel >= 1:2.6.0
BuildRequires:	meson >= 1.8.1-2
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 2.042
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	libudfread >= 1.2.0
Requires:	libxml2 >= 1:2.6.0
%if %{with java}
BuildRequires:	ant
%buildrequires_jdk
Provides:	%{name}(jvm) = %{version}-%{release}
Suggests:	%{name}-java = %{version}-%{release}
%endif
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
Requires:	fontconfig-devel
Requires:	freetype-devel >= 2
Requires:	libudfread-devel >= 1.2.0
Requires:	libxml2-devel >= 1:2.6.0

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

%package java
Summary:	BD-Java support classes for libbluray
Summary(pl.UTF-8):	Klasy obsługujące BD-Java dla libbluray
Group:		Libraries/Java
Requires:	%{name}(jvm) = %{version}-%{release}
Requires:	jre

%description java
BD-Java support classes for libbluray.

%description java -l pl.UTF-8
Klasy obsługujące BD-Java dla libbluray.

%package apidocs
Summary:        API documentation for libbluray library
Summary(pl.UTF-8):      Dokumentacja API biblioteki libbluray
Group:          Documentation
BuildArch:      noarch

%description apidocs
API documentation for libbluray library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libbluray.

%prep
%setup -q

%build
%if %{with java}
export JAVA_HOME="%{java_home}"
export JAVAC="%{java_home}/bin/javac"
%endif
%meson \
	%{!?with_static_libs:--default-library=shared} \
%if %{with java}
	-Dbdj_jar=enabled \
	-Djdk_home="%{java_home}" \
%if %{_ver_ge %default_jdk_version 9}
	-Djava9=true \
%else
	-Djava9=false \
%endif
%else
	-Dbdj_jar=disabled \
%endif
	-Denable_docs=%{__true_false apidocs} \
	-Dfontconfig=enabled \
	-Dfreetype=enabled \
	-Dlibxml2=enabled

%meson_build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

%{?with_apidocs:%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/doc/libbluray}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog README.md
%attr(755,root,root) %{_bindir}/bd_info
%attr(755,root,root) %{_bindir}/bd_list_titles
%attr(755,root,root) %{_bindir}/bd_splice
%attr(755,root,root) %{_libdir}/libbluray.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libbluray.so.3

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

%if %{with java}
# NOTE: it's Java package loaded by libbluray itself, not Java API to libbluray
# thus -java instead of java- namespace.
%files java
%defattr(644,root,root,755)
%{_javadir}/libbluray-awt-j2se-%{version}.jar
%{_javadir}/libbluray-j2se-%{version}.jar
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc build/doc/html/*
%endif
