# TODO
# - add other browsers (opera, google-chrome, firefox...)
Summary:	LastPass binary version to enable sharing login state between other browsers
Name:		browser-plugin-lastpass
Version:	3.1.10
Release:	0.2
License:	?
Group:		X11/Applications/Networking
Source0:	https://lastpass.com/lplinux.tar.bz2
# Source0-md5:	eedb4dcf4f44ba80c4531514aec4d38f
NoSource:	0
Source1:	https://lastpass.com/lpchrome_linux.crx
# Source1-md5:	b1bd0fd75b38ba34b2cbd605746d5e83
NoSource:	1
URL:		https://lastpass.com/
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

#%define		chromium_cfdir	/etc/chromium-browser
# FIXME: currently (chrome<34) chromium config dir is wrong: /etc/chromium not /etc/chromium-browser
%define		chromium_cfdir	/etc/chromium

%ifarch %{x8664}
%define		NPLASTPASS nplastpass64
%else
%define		NPLASTPASS nplastpass
%endif

%description
Binary version of LastPass to enable importing passwords from Google
Chrome password manager and to enable sharing login state between
other browsers.

%prep
%setup -qc

echo "{ \"ExtensionInstallSources\": [\"https://lastpass.com/*\", \"https://*.lastpass.com/*\", \"https://*.cloudfront.net/lastpass/*\"] }" \
	> lastpass_policy.json
echo "{ \"name\": \"com.lastpass.nplastpass\", \"description\": \"LastPass\", \"path\": \"%{chromium_cfdir}/native-messaging-hosts/%{NPLASTPASS}\", \"type\": \"stdio\", \"allowed_origins\": [ \"chrome-extension://hdokiejnpimakedhajhdlcegeplioahd/\", \"chrome-extension://debgaelkhoipmbjnhpoblmbacnmmgbeg/\" ] }" \
	> com.lastpass.nplastpass.json

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{chromium_cfdir}/{policies/managed,native-messaging-hosts}
cp -p lastpass_policy.json $RPM_BUILD_ROOT%{chromium_cfdir}/policies/managed
cp -f %{NPLASTPASS} $RPM_BUILD_ROOT%{chromium_cfdir}/native-messaging-hosts
cp -p com.lastpass.nplastpass.json $RPM_BUILD_ROOT%{chromium_cfdir}/native-messaging-hosts

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
# FIXME: should be owned by chromium itself
%dir %{chromium_cfdir}
%dir %{chromium_cfdir}/native-messaging-hosts
%dir %{chromium_cfdir}/policies
%dir %{chromium_cfdir}/policies/managed
%config(noreplace) %verify(not md5 mtime size) %{chromium_cfdir}/policies/managed/lastpass_policy.json
%config(noreplace) %verify(not md5 mtime size) %{chromium_cfdir}/native-messaging-hosts/com.lastpass.nplastpass.json
%attr(755,root,root) %{chromium_cfdir}/native-messaging-hosts/nplastpass64
