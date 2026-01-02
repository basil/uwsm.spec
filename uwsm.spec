Name:           uwsm
Summary:        Universal Wayland Session Manager
Version:        0.26.0
Release:        1%{?dist}

License:        MIT
URL:            https://github.com/Vladimir-csp/%{name}
Source:         %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  desktop-file-utils
BuildRequires:  meson
BuildRequires:  python3
BuildRequires:  python3-dbus
BuildRequires:  python3-pyxdg
BuildRequires:  python-rpm-macros
BuildRequires:  scdoc
BuildRequires:  systemd-rpm-macros

Requires:       python3
Requires:       python3-dbus
Requires:       python3-pyxdg
Requires:       util-linux

Recommends:     /usr/bin/notify-send
Recommends:     /usr/bin/whiptail
Recommends:     wofi

%description
Provides a set of Systemd units and helpers to set up the environment
and manage standalone Wayland compositor sessions.

Aside from environment setup/cleanup, it makes Systemd do most of the
work and does not require any extra daemons running in background
(except for a tiny waitpid process and a simple shell signal handler in
the lightest case).

This setup provides robust session management, overridable compositor-
and session-aware environment management, XDG autostart, bi-directional
binding with login session, clean shutdown, solutions for a set of small
but annoying gotchas of systemd session management.

For compositors this is an opportunity to offload: Systemd integration,
session/XDG autostart management, Systemd/DBus activation environment
interaction with its caveats.

%prep
%autosetup -p1

%build
%meson -Duuctl=enabled -Dfumon=enabled -Dfumon-preset=disabled -Dwait-tray=enabled -Duwsm-app=enabled
%meson_build

%install
%meson_install
%py_byte_compile %{python3} %{buildroot}%{_datadir}/%{name}/modules

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop

%post
%systemd_user_post fumon.service

%preun
%systemd_user_preun fumon.service

%postun
%systemd_user_postun fumon.service

%files
%doc %{_docdir}/%{name}/
%license LICENSE
%{_bindir}/fumon
%{_bindir}/%{name}
%{_bindir}/%{name}-app
%{_bindir}/%{name}-terminal
%{_bindir}/%{name}-terminal-scope
%{_bindir}/%{name}-terminal-service
%{_bindir}/uuctl
%{_bindir}/wait-tray
%{_datadir}/applications/uuctl.desktop
%{_datadir}/%{name}/
%{_libexecdir}/%{name}/prepare-env.sh
%{_libexecdir}/%{name}/signal-handler.sh
%{_mandir}/man1/fumon.1.*
%{_mandir}/man1/uuctl.1.*
%{_mandir}/man1/%{name}.1.*
%{_mandir}/man1/%{name}-app.1.*
%{_mandir}/man3/%{name}-plugins.3.*
%{_userpresetdir}/80-fumon.preset
%{_userunitdir}/*-graphical.slice
%{_userunitdir}/fumon.service
%{_userunitdir}/wayland-*.service
%{_userunitdir}/wayland-*.target

%changelog
* Fri Jan 2 2026 Basil Crow <me@basilcrow.com> - 0.26.0-1
- Initial packaging
