# vim: foldmethod=marker

%global debug_package %{nil}

%global _QT_PLUGINS %{_libdir}/qt4/plugins
%global _QCAD_DIR %{_datadir}/%{name}

Name:           qcad
# See R_QCAD_VERSION_STRING in src/core/RVersion.h
Version:        3.15.4.1
Release:        1%{?dist}

# {{{1 package meta-data
# {{{2 package meta-data [base]
Summary:        a crossplatform 2D CAD solution that supports the DXF format

License:        GPLv3
URL:            http://www.qcad.org
# https://github.com/qcad/qcad/archive/v%{version}.zip
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  desktop-file-utils
BuildRequires:  qt-devel >= 4.8.4 pkgconfig(QtWebKit)

Requires(post):     desktop-file-utils
Requires(postun):   desktop-file-utils


Requires:       qt-designer-plugin-webkit >= 4.8.4

%description
QCAD is an application for computer aided drafting (CAD) in two dimensions
(2D).  With QCAD you can create technical drawings such as plans for
buildings, interiors, mechanical parts or schematics and diagrams.

# {{{2 package meta-data [examples]
%package examples

Summary:        QCAD example drawings

Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description examples
This provides example drawings that you can load into QCAD.


# {{{2 package meta-data [example-library]
%package example-library

Summary:        QCAD example library
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description example-library
This provides example part libraries for use with QCAD.


# {{{2 package meta-data [templates]
%package        templates

Summary:        QCAD templates
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description templates
This provides some basic templates for use with QCAD.


# {{{2 package meta-data [translations]
%package translations

Summary:        QCAD language translations

Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description translations
This provides language translations for use by QCAD.



# {{{1 prep & build
%prep
%setup -q

%build
qmake-qt4 -r \
	QMAKE_CFLAGS+="%{optflags}" \
	QMAKE_CXXFLAGS+="%{optflags}"
make %{?_smp_mflags}

# {{{1 install
%install

install -d -m 0755 %{buildroot}/%{_QCAD_DIR}

for _dir in examples fonts libraries linetypes patterns plugins scripts \
            themes ts
do
    cp --preserve=timestamps --recursive $_dir %{buildroot}/%{_QCAD_DIR}
done

install -Dp -m 0644 scripts/qcad_icon.png \
	%{buildroot}/%{_datadir}/pixmaps/%{name}.png
install -Dp -m 0644 scripts/qcad_icon.svg \
	%{buildroot}/%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

ln -s %{_QT_PLUGINS}/codecs/*.so \
	%{buildroot}/%{_QCAD_DIR}/plugins/codecs/
ln -s %{_QT_PLUGINS}/designer/libqwebview.so \
	%{buildroot}/%{_QCAD_DIR}/plugins/designer/
ln -s %{_QT_PLUGINS}/imageformats/*.so \
	%{buildroot}/%{_QCAD_DIR}/plugins/imageformats/
ln -s %{_QT_PLUGINS}/sqldrivers/*.so \
	%{buildroot}/%{_QCAD_DIR}/plugins/sqldrivers/

find %{buildroot}/%{_QCAD_DIR} -name "*.pri" -delete
find %{buildroot}/%{_QCAD_DIR} -name "*.pro" -delete
find %{buildroot}/%{_QCAD_DIR} -name "*.ts" -delete
find %{buildroot}/%{_QCAD_DIR} -name "Makefile" -delete
find %{buildroot}/%{_QCAD_DIR} -name ".gitignore" -delete

install -d -m 0755 %{buildroot}/%{_bindir}
cat <<EOF > %{buildroot}/%{_bindir}/qcad
#!/bin/sh
LD_LIBRARY_PATH=/%{_QCAD_DIR}:\$LD_LIBRARY_PATH /%{_QCAD_DIR}/qcad-bin "\$@"
EOF
chmod 0755 %{buildroot}/%{_bindir}/qcad

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
        --add-category X-Fedora                     \
        --add-category Application                  \
        --add-category Graphics                     \
        --dir %{buildroot}%{_datadir}/applications  \
        %{name}.desktop

# {{{1 post
%post
%{_bindir}/update-desktop-database %{_datadir}/applications &> /dev/null || :

# {{{1 postun
%postun
%{_bindir}/update-desktop-database %{_datadir}/applications &> /dev/null || :

# {{{1 files
# {{{2 files [base]
%files
%defattr(-,root,root,-)

%doc cc-by-3.0.txt gpl-3.0-exceptions.txt gpl-3.0.txt LICENSE.txt
/%{_QCAD_DIR}
%{_bindir}/%{name}
%{_datadir}/pixmaps/qcad.png
%{_datadir}/applications/qcad.desktop
%{_datadir}/icons/hicolor/scalable/apps/qcad.svg
%exclude /%{_QCAD_DIR}/lib*.a
%exclude /%{_QCAD_DIR}/examples
%exclude /%{_QCAD_DIR}/ts
%exclude /%{_QCAD_DIR}/libraries/templates
%exclude /%{_QCAD_DIR}/libraries/default


# {{{2 files [examples]
%files examples
%defattr(-,root,root,-)

/%{_QCAD_DIR}/examples


# {{{2 files [example-library]
%files example-library
%defattr(-,root,root,-)
/%{_QCAD_DIR}/libraries/default


# {{{2 files [templates]
%files templates
%defattr(-,root,root,-)
/%{_QCAD_DIR}/libraries/templates


# {{{2 files [translations]
%files translations
%defattr(-,root,root,-)
/%{_QCAD_DIR}/ts



# {{{1 changelog
%changelog
* Mon Aug 01 2016 John Florian <jflorian@doubledog.org> 3.15.4.1-1
- new package built with tito

