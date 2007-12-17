# pretty borked...
%define major 8.1
%define tcl_major 8.5
%define tk_major  8.5
%define libname	%mklibname tix %{major}.%{tcl_major}

Summary:	A set of capable widgets for Tk
Name:		tix
Version:	8.1.4
Release:	%mkrel 6
License:	BSD
Group:		System/Libraries
URL:		http://tix.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/tixlibrary/tix-%{version}.tar.bz2
Patch10:	tix-8.1.4-install-pkgIndex-datadir-83662.patch
Patch11:	tix-8.1.4-pkgIndex-datadir-83662.patch
Patch1:     tix-8.1.4-tcl85.patch 
BuildRequires:	tcl-devel
BuildRequires:	tk-devel
BuildRequires:	groff
BuildRequires:	tcl
BuildRequires:	libxscrnsaver-devel
Epoch:		1

%description
Tix (Tk Interface Extension), an add-on for the Tk widget set, is an
extensive set of over 40 widgets.  In general, Tix widgets are more
complex and more capable than the widgets provided in Tk.  Tix widgets
include a ComboBox, a Motif-style FileSelectBox, an MS Windows-style
FileSelectBox, a PanedWindow, a NoteBook, a hierarchical list, a
directory tree and a file manager.

Install the tix package if you want to try out more complicated widgets
for Tk.  You'll also need to have the tcl and tk packages installed.

%package -n	%{libname}
Summary:	Shared libraries for %{name}
Group:		System/Libraries
Epoch:		1

%description -n %{libname}
Tix (Tk Interface Extension), an add-on for the Tk widget set, is an
extensive set of over 40 widgets.  In general, Tix widgets are more
complex and more capable than the widgets provided in Tk.  Tix widgets
include a ComboBox, a Motif-style FileSelectBox, an MS Windows-style
FileSelectBox, a PanedWindow, a NoteBook, a hierarchical list, a
directory tree and a file manager.

Install the tix package if you want to try out more complicated widgets
for Tk.  You'll also need to have the tcl and tk packages installed.

%package -n	%{libname}-devel 
Summary:	Development files for %{name}
Group:		Development/Other
Requires:	%{libname} = 1:%{version}
Provides:	%{name}-devel = 1:%{version}-%{release}
Provides:	lib%{name}-devel = 1:%{version}-%{release}
Epoch:		1

%description -n	%{libname}-devel
This package contains development files for %{name}.

%prep

%setup -q
%patch10 -p0
%patch11 -p0
%patch1 -p0
# patch makefile to BINDIRS
perl -pi -e 's/(BINDIRS\s*= )/$1 tk8.5 /g' unix/Makefile.in
# clean up CVS stuff
for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -r $i; fi >&/dev/null
done
    
# fix dir perms
find docs -type d | xargs chmod 755
    
# fix file perms
find docs  -type f | xargs chmod 644
    
# nuke pdf files
rm -rf docs/pdf

%build
for f in config.guess config.sub ; do
    test -f /usr/share/libtool/$f || continue
    find . -type f -name $f -exec cp /usr/share/libtool/$f \{\} \;
done

pushd unix

    # source these (easier)
    . %{_libdir}/tclConfig.sh
    . %{_libdir}/tkConfig.sh

#    export SHLIB_VERSION=%{version}

    %configure \
	--enable-gcc \
	--enable-shared \
        --with-tclconfig=%{_libdir} \
        --with-tkconfig=%{_libdir} \
        --with-tclinclude=$TCL_SRC_DIR \
        --with-tkinclude=$TK_SRC_DIR
    cp -r tk8.4 tk%tk_major
    pushd tk%tk_major
    perl -pi -e 's/8.4/%tk_major/' Makefile
	%configure \
    	    --enable-gcc \
            --enable-shared \
            --with-tclconfig=%{_libdir} \
            --with-tkconfig=%{_libdir} \
            --with-tclinclude=$TCL_SRC_DIR \
            --with-tkinclude=$TK_SRC_DIR
	# works without a patch, amazing!
        %make SHLIB_LD="gcc -pipe -shared -Wl,-soname=libtix%{major}.%{tcl_major}.so.0"
    popd

popd

%install
rm -rf %{buildroot}

# If %{_libdir} is not %{_prefix}/lib, then define EXTRA_TCLLIB_FILES
# which contains actual non-architecture-dependent tcl code.
if [ "%{_libdir}" != "%{_prefix}/lib" ]; then
    EXTRA_TCLLIB_FILES="%{buildroot}%{_prefix}/lib/*"
fi

install -d %{buildroot}%{_libdir}
install -d %{buildroot}%{_datadir}/%{name}%{major} 
install -d %{buildroot}%{_includedir}/%{name}%{major} 

%makeinstall -C unix \
    LIB_DIR=%{buildroot}%{_libdir} \
    MAN_DIR=%{buildroot}%{_mandir} \
    TIX_LIBRARY=%{buildroot}%{_datadir}/%{name}%{major} \
    TCL_BIN_DIR=%{_bindir}

# install all headers
install -d %{buildroot}%{_includedir}/%{name}%{version}/generic
install -d %{buildroot}%{_includedir}/%{name}%{version}/unix
install -m0644 generic/*.h %{buildroot}%{_includedir}/%{name}%{version}/generic/
install -m0644 unix/*.h %{buildroot}%{_includedir}/%{name}%{version}/unix/

# Not needed anymore?
rm -rf %{buildroot}%{_libdir}/libtixsam*.so*

# fix the shared libname
rm -f %{buildroot}%{_libdir}/libtix*.so
install -m0755 unix/tk%tk_major/libtix%{major}.%{tcl_major}.so %{buildroot}%{_libdir}/libtix%{major}.%{tcl_major}.so.0
ln -snf libtix%{major}.%{tcl_major}.so.0 %{buildroot}%{_libdir}/libtix%{major}.%{tcl_major}.so

pushd %{buildroot}%{_bindir}
    ln -s tixwish%{major}.%{tcl_major} tixwish
popd

# tixwish.1 in /usr/share/man/man1.
mv %{buildroot}/usr/share/man/mann/tixwish.1 %{buildroot}/usr/share/man/man1
	
# (fc) make sure .so files are writable by root
chmod 755 %{buildroot}%{_libdir}/*.so*

# fix the tixConfig.sh file
perl -pi -e "s|`pwd`/unix/tk%tk_major|%{_libdir}|g" %{buildroot}%{_libdir}/tixConfig.sh

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc *.txt *.html license.terms docs/*
%attr(0755,root,root) %{_bindir}/*
%{_datadir}/%{name}%{major}
%{_libdir}/%{name}%{major}
%{_mandir}/man1/*

%files -n %{libname}
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/lib*.so.*

%files -n %{libname}-devel
%defattr(-,root,root,-)
%dir %{_includedir}/%{name}%{version}
%dir %{_includedir}/%{name}%{version}/generic
%dir %{_includedir}/%{name}%{version}/unix
%{_includedir}/%{name}%{version}/generic/*.h
%{_includedir}/%{name}%{version}/unix/*.h
%{_includedir}/*.h
%{_libdir}/tixConfig.sh
%attr(0755,root,root) %{_libdir}/*.so
%{_mandir}/mann/*


