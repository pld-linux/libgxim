#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	static_libs	# don't build static libraries
#
Summary:	GObject-based XIM protocol library
Summary(pl.UTF-8):	Biblioteka protokołu XIM oparta na GObject
Name:		libgxim
Version:	0.5.0
Release:	6
License:	LGPL v2+
Group:		Libraries
Source0:	http://bitbucket.org/tagoh/libgxim/downloads/%{name}-%{version}.tar.bz2
# Source0-md5:	4bb1fa63d00eb224439d413591c29a6a
Patch0:		format-security.patch
URL:		http://tagoh.bitbucket.org/libgxim/
BuildRequires:	dbus-devel >= 0.23
BuildRequires:	dbus-glib-devel >= 0.74
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.32.0
BuildRequires:	gtk-doc >= 1.8
BuildRequires:	gtk+2-devel >= 2:2.2.0
BuildRequires:	intltool
BuildRequires:	pkgconfig
BuildRequires:	ruby
BuildRequires:	xorg-lib-libX11-devel
Requires:	dbus-libs >= 0.23
Requires:	dbus-glib >= 0.74
Requires:	glib2 >= 1:2.32.0
Requires:	gtk+2 >= 2:2.2.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libgxim is a X Input Method protocol library that is implemented by
GObject. This library helps you to implement XIM servers or client
applications to communicate through XIM protocol without using Xlib
API directly, particularly if your application uses GObject-based main
loop.

%description -l pl.UTF-8
libgxim to biblioteka protokołu X Input Method zaimplementowana w
oparciu o GObject. Biblioteka ta pozwala na implementowanie serwerów
lub aplikacji klienckich XIM komunikających się przy użyciu protokołu
XIM bez używania bezpośrednio API Xlib, w szczególności kiedy
aplikacja wykorzystuje główną pętlę opartą na GObject.

%package devel
Summary:	Header files for libgxim library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libgxim
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	dbus-devel >= 0.23
Requires:	dbus-glib-devel >= 0.74
Requires:	glib2-devel >= 1:2.32.0
Requires:	gtk+2-devel >= 2:2.2.0

%description devel
Header files for libgxim library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libgxim.

%package static
Summary:	Static libgxim library
Summary(pl.UTF-8):	Statyczna biblioteka libgxim
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libgxim library.

%description static -l pl.UTF-8
Statyczna biblioteka libgxim.

%package apidocs
Summary:	libgxim API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki libgxim
Group:		Documentation

%description apidocs
API and internal documentation for libgxim library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libgxim.

%prep
%setup -q
%patch0 -p1

%build
%configure \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static} \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

# only empty translations exist (as of 0.5.0)
#%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

#%files -f %{name}.lang
%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_libdir}/libgxim.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgxim.so.4

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgxim.so
%{_includedir}/libgxim
%{_pkgconfigdir}/libgxim.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libgxim.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libgxim
%endif
