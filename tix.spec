Summary:	A set of capable widgets for Tk
Name:		tix
Version:	8.4.3
Release:	13
Epoch:		1
License:	BSD
Group:		System/Libraries
URL:		http://tix.sourceforge.net/
Source0:	http://downloads.sourceforge.net/tixlibrary/Tix%{version}-src.tar.gz
Source1:	%{name}.rpmlintrc
Patch1:		tix-8.4.2-link.patch
Patch2:		tix-8.4.3-tcl86.patch
BuildRequires:	tcl-devel
BuildRequires:	tk-devel
BuildRequires:	groff
BuildRequires:	tcl
BuildRequires:	pkgconfig(xscrnsaver)

%description
Tix (Tk Interface Extension), an add-on for the Tk widget set, is an
extensive set of over 40 widgets.  In general, Tix widgets are more
complex and more capable than the widgets provided in Tk.  Tix widgets
include a ComboBox, a Motif-style FileSelectBox, an MS Windows-style
FileSelectBox, a PanedWindow, a NoteBook, a hierarchical list, a
directory tree and a file manager.

Install the tix package if you want to try out more complicated widgets
for Tk.  You'll also need to have the tcl and tk packages installed.

%package	devel
Summary:	Development files for %{name}
Group:		Development/Other

%description	devel
This package contains development files for %{name}.

%prep
%setup -q -n Tix%{version}
%patch1 -p1 -b .link
%patch2 -p1 -b .tcl86

# nuke pdf files
rm -rf docs/pdf

%build
for f in config.guess config.sub ; do
    test -f /usr/share/libtool/$f || continue
    find . -type f -name $f -exec cp /usr/share/libtool/$f \{\} \;
done

%configure2_5x --libdir=%{tcl_sitearch}
%make PKG_LIB_FILE=libTix.so

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}
install -d %{buildroot}%{tcl_sitearch}
install -d %{buildroot}%{_includedir}/%{name}

%makeinstall_std PKG_LIB_FILE=libTix.so

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



%changelog
* Fri May 06 2011 Oden Eriksson <oeriksson@mandriva.com> 1:8.4.3-5mdv2011.0
+ Revision: 670708
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 1:8.4.3-4mdv2011.0
+ Revision: 608005
- rebuild

* Mon Mar 15 2010 Oden Eriksson <oeriksson@mandriva.com> 1:8.4.3-3mdv2010.1
+ Revision: 520286
- rebuilt for 2010.1

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 1:8.4.3-2mdv2010.0
+ Revision: 427379
- rebuild

* Sat Dec 06 2008 Adam Williamson <awilliamson@mandriva.org> 1:8.4.3-1mdv2009.1
+ Revision: 311053
- rebuild for new tcl
- install to new location as per policy, but also to /usr/lib as tix binary
  is linked against the lib
- drop a bunch of old silly workarounds
- drop old patches (no longer needed)
- add tcl86.patch (fix build for tcl 8.6)
- add link.patch (from Fedora, I think)
- new release 8.4.3
- drop all the ridiculous libification crap

* Mon Sep 15 2008 Per Øyvind Karlsen <peroyvind@mandriva.org> 1:8.1.4-9mdv2009.0
+ Revision: 284835
- rebuild to fix 'rpmlib(PayloadIsLzma) <= 4.4.2.2-1' dependency

* Wed Jun 18 2008 Thierry Vignaud <tv@mandriva.org> 1:8.1.4-8mdv2009.0
+ Revision: 225753
- rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Wed Mar 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1:8.1.4-7mdv2008.1
+ Revision: 179652
- rebuild

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Fri Sep 07 2007 Anssi Hannula <anssi@mandriva.org> 1:8.1.4-6mdv2008.0
+ Revision: 82018
- rebuild for new soname of tcl

* Tue May 15 2007 Michael Scherer <misc@mandriva.org> 1:8.1.4-5mdv2008.0
+ Revision: 26805
- Fix BuildRequires
- rebuild on new tcl 8.5


* Fri Feb 02 2007 Oden Eriksson <oeriksson@mandriva.com> 8.1.4-4mdv2007.0
+ Revision: 115965
- Import tix

* Thu Jan 19 2006 Christiaan Welvaart <cjw@daneel.dyndns.org> 1:8.1.4-4mdk
- add BuildRequires: tcl (for tclsh)

* Tue Jan 03 2006 Oden Eriksson <oeriksson@mandriva.com> 1:8.1.4-3mdk
- fix deps

* Tue Jan 03 2006 Oden Eriksson <oeriksson@mandriva.com> 1:8.1.4-2mdk
- added epoch

* Sun Jan 01 2006 Oden Eriksson <oeriksson@mandriva.com> 8.1.4-1mdk
- initial Mandriva package

