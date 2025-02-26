Summary:	A set of capable widgets for Tk
Name:		tix
Version:	8.4.3
Release:	18
Epoch:		1
License:	BSD
Group:		System/Libraries
URL:		https://tix.sourceforge.net/
Source0:	http://downloads.sourceforge.net/tixlibrary/Tix%{version}-src.tar.gz
Source1:	%{name}.rpmlintrc
Patch1:		https://src.fedoraproject.org/rpms/tix/raw/master/f/tix-8.4.2-link.patch
Patch2:		https://src.fedoraproject.org/rpms/tix/raw/master/f/tix-8.4.3-tcl86.patch
Patch3:		https://src.fedoraproject.org/rpms/tix/raw/master/f/tix-8.4.3-covscan-fixes.patch
BuildRequires:	pkgconfig(tcl)
BuildRequires:	pkgconfig(tk)
BuildRequires:	groff
BuildRequires:	pkgconfig(xscrnsaver)

%description
Tix (Tk Interface Extension), an add-on for the Tk widget set, is an
extensive set of over 40 widgets.  In general, Tix widgets are more
complex and more capable than the widgets provided in Tk.  Tix widgets
include a ComboBox, a Motif-style FileSelectBox, an MS Windows-style
FileSelectBox, a PanedWindow, a NoteBook, a hierarchical list, a
directory tree and a file manager.

Install the tix package if you want to try out more complicated widgets
for Tk. You'll also need to have the tcl and tk packages installed.

%package devel
Summary:	Development files for %{name}
Group:		Development/Other
Requires:	%{name} = %{EVRD}

%description devel
This package contains development files for %{name}.

%prep
%autosetup -n Tix%{version} -p1

# nuke pdf files
rm -rf docs/pdf

%build
for f in config.guess config.sub ; do
    test -f /usr/share/libtool/$f || continue
    find . -type f -name $f -exec cp /usr/share/libtool/$f \{\} \;
done

%configure \
	--libdir=%{tcl_sitearch} \
	--with-tcl=%{_libdir} \
	--with-tk=%{_libdir}

%make_build PKG_LIB_FILE=libTix.so

%install
install -d %{buildroot}%{_libdir}
install -d %{buildroot}%{tcl_sitearch}
install -d %{buildroot}%{_includedir}/%{name}

%make_install PKG_LIB_FILE=libTix.so

# put the library in /usr/lib as Tix itself is directly linked
mv %{buildroot}%{tcl_sitearch}/Tix%{version}/libTix.so %{buildroot}%{_libdir}
ln -s %{_libdir}/libTix.so %{buildroot}%{tcl_sitearch}/Tix%{version}/libTix.so

# install all headers
install -d %{buildroot}%{_includedir}/%{name}/generic
install -d %{buildroot}%{_includedir}/%{name}/unix
install -m0644 generic/*.h %{buildroot}%{_includedir}/%{name}/generic/
install -m0644 unix/*.h %{buildroot}%{_includedir}/%{name}/unix/

# install man pages
mkdir -p %{buildroot}%{_mandir}/mann
mkdir -p %{buildroot}%{_mandir}/man1
install -m0644 man/*.n %{buildroot}%{_mandir}/mann
install -m0644 man/*.1 %{buildroot}%{_mandir}/man1

# remove stuff that ends up as docs
rm -f %{buildroot}%{tcl_sitearch}/Tix%{version}/README.txt
rm -f %{buildroot}%{tcl_sitearch}/Tix%{version}/license.terms

%files
%doc *.txt *.html license.terms docs/*
%{_libdir}/libTix.so
%{tcl_sitearch}/Tix%{version}
%{_mandir}/man1/*

%files devel
%{_includedir}/%{name}
%{_mandir}/mann/*
