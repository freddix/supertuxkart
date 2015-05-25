%define		pre rc1
Summary:	Free 3d kart racing game
Name:		supertuxkart
Version:	0.9
Release:	0.%{pre}.1
License:	GPL v1, GPL v2, GPL v3+, CC-BY-SA v3, CC-BY-SA v3+
Group:		X11/Applications/Games
Source0:	http://downloads.sourceforge.net/supertuxkart/%{name}-%{version}%{pre}-src.tar.7z
# Source0-md5:	4d8ee6f7093f819bafc0be95a75f05b2
URL:		http://supertuxkart.net/
BuildRequires:	OpenGL-devel
BuildRequires:	OpenGL-glut-devel
BuildRequires:	SDL-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bzip2-devel
BuildRequires:	fribidi-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libvorbis-devel
BuildRequires:	openal-soft-devel
BuildRequires:	pkg-config
BuildRequires:	unzip
BuildRequires:	xorg-libXxf86vm-devel
Requires(post,postun):	/usr/bin/gtk-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SuperTuxKart is an enhanced version of TuxKart, a kart racing game,
originaly done by Steve Baker, featuring Tux and a bunch of his
friends.

%prep
rm -rf %{name}-%{version}%{pre}
7z x %{SOURCE0}

cd %{name}-%{version}%{pre}
%{__rm} -r lib/{jpeglib,libpng,zlib}

%build
cd %{name}-%{version}%{pre}
%if 0
_srcdir=$(pwd)
cd lib/irrlicht/source/Irrlicht
export CC="%{__cc}"
export CFLAGS="%{rpmcflags}"
export CXX="%{__cxx}"
export CXXFLAGS="%{rpmcxxflags}"
export LDFLAGS="%{rpmldflags}"
%{__make} NDEBUG=1
cd $_srcdir
%endif

mkdir build
cd build
%cmake .. \
	-DIRRLICHT_DIR="$_srcdir/irrlicht"  \
	-DBUILD_SHARED_LIBS=OFF		    \
	-DUSE_WIIUSE=0

%install
rm -rf $RPM_BUILD_ROOT
cd %{name}-%{version}%{pre}
install -d $RPM_BUILD_ROOT%{_desktopdir}

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_datadir}/supertuxkart/data/run_me.sh
find $RPM_BUILD_ROOT%{_datadir}/supertuxkart -name Makefile* -exec rm -f {} \;

cat > $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop <<EOF
[Desktop Entry]
Type=Application
Exec=%{name} --log=file
Icon=%{name}
Terminal=false
Name=SuperTuxKart
Comment=3D kart racing game
StartupNotify=false
Categories=Game;ArcadeGame;
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor

%postun
%update_icon_cache hicolor

%files
%defattr(644,root,root,755)
#%doc ChangeLog README TODO data/CREDITS
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}
%{_desktopdir}/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/*.png

