Summary:	Saleae Logic Analyzer Software
Name:		saleae-logic
Version:	0.1.18
Release:	1
License:	Commercial
Group:		X11/Applications/Graphics
Source0:	http://downloads.saleae.com/betas/1.1.18/Logic+1.1.18+(32-bit).zip
NoSource:	0
Source1:	http://downloads.saleae.com/betas/1.1.18/Logic+1.1.18+(64-bit).zip
NoSource:	1
Source2:	%{name}-udev.rules
URL:		http://www.saleae.com/logic16/features
BuildRequires:	unzip
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Saleae Logic Analyzer Software.

%prep
%setup -qcT
%ifarch %{ix86}
SOURCE=%{S:0}
%endif
%ifarch %{x8664}
SOURCE=%{S:1}
%endif

unzip -q ${SOURCE}

%build

%install
rm -rf $RPM_BUILD_ROOT

cd Logic*

install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/%{name},/lib/udev/rules.d/}

chmod 755 Analyzers/*.so libAnalyzer.so Logic
cp -a Analyzers Errors Settings libAnalyzer.so Logic $RPM_BUILD_ROOT%{_libdir}/%{name}

install %{SOURCE2} $RPM_BUILD_ROOT/lib/udev/rules.d/saleae-logic.rules

cat << 'EOF' >> $RPM_BUILD_ROOT%{_bindir}/saleae-logic
#!/bin/sh
if [ ! -d ~/.saleae-logic ]; then
	mkdir ~/.saleae-logic
	mkdir ~/.saleae-logic/Errors
	mkdir ~/.saleae-logic/Settings
	for f in Analyzers libAnalyzer.so; do
		ln -s %{_libdir}/%{name}/$f ~/.saleae-logic/$f
	done
	ln %{_libdir}/%{name}/Logic ~/.saleae-logic/ 2> /dev/null || cp -a %{_libdir}/%{name}/Logic ~/.saleae-logic/
fi
cd ~/.saleae-logic
exec ./Logic
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Logic*/{License,linux_readme}.txt
%attr(755,root,root) %{_bindir}/saleae-logic
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/Analyzers
%attr(755,root,root) %{_libdir}/%{name}/Analyzers/*.so
%{_libdir}/%{name}/Errors
%attr(755,root,root) %{_libdir}/%{name}/Logic
%attr(755,root,root) %{_libdir}/%{name}/libAnalyzer.so
%{_libdir}/%{name}/Settings
/lib/udev/rules.d/saleae-logic.rules
