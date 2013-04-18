Summary:	Free 3d kart racing game
Name:		supertuxkart
Version:	0.8
Release:	3
License:	GPL v1, GPL v2, GPL v3+, CC-BY-SA v3, CC-BY-SA v3+
Group:		X11/Applications/Games
Source0:	http://downloads.sourceforge.net/supertuxkart/%{name}-%{version}-src.tar.bz2
# Source0-md5:	0b939ce601374758938119e0b0dd1fec
Patch0:		%{name}-system-libs.patch
URL:		http://supertuxkart.net/
BuildRequires:	ImageMagick-coders
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
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SuperTuxKart is an enhanced version of TuxKart, a kart racing game,
originaly done by Steve Baker, featuring Tux and a bunch of his
friends.

%prep
%setup -qn SuperTuxKart-%{version}
%patch0 -p1

%{__rm} -r lib/irrlicht/source/Irrlicht/{bzip2,jpeglib,libpng,zlib}

%build
_srcdir=$(pwd)
cd lib/irrlicht/source/Irrlicht
export CC="%{__cc}"
export CFLAGS="%{rpmcflags}"
export CXX="%{__cxx}"
export CXXFLAGS="%{rpmcxxflags}"
export LDFLAGS="%{rpmldflags}"
%{__make} NDEBUG=1
cd $_srcdir

mkdir build
cd build
%cmake .. \
	-DIRRLICHT_DIR="$_srcdir/irrlicht"	\
	-DBUILD_SHARED_LIBS:BOOL=OFF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_desktopdir}

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_datadir}/supertuxkart/data/{*.xpm,run_me.sh,supertuxkart_desktop.template}
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

convert data/supertuxkart_64.xpm $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}.png

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog README TODO data/CREDITS
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}
%{_desktopdir}/%{name}.desktop
%{_pixmapsdir}/%{name}.png

