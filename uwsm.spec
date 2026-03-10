Name:           uwsm
Summary:        Universal Wayland Session Manager
Version:        0.26.1
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
Wayland session manager for standalone compositors
uwsm (Universal Wayland Session Manager) provides a lightweight, modular
session management framework for Wayland environments based on systemd user
units and various helpers.

It handles various session-related tasks for standalone Wayland compositors,
such as:

- startup from login shell or DM
- dynamic loading and cleanup of environment variables for graphical session
- binding lifetime of graphical session and login session together

It sets the stage for systemd to do launch and lifecycle management,
XDG autostart, clean shutdown.

dbus-broker is recommended for better systemd integration and environment
cleanup.

%prep
%autosetup -p1

%build
%meson -Duuctl=enabled -Dfumon=enabled -Dfumon-preset=disabled -Dwait-tray=enabled -Duwsm-app=enabled
%meson_build

%install
%meson_install
# Systemd presets are not permitted except in fedora-release
rm -f %{buildroot}%{_userpresetdir}/80-fumon.preset
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
%{_userunitdir}/*-graphical.slice
%{_userunitdir}/fumon.service
%{_userunitdir}/wayland-*.service
%{_userunitdir}/wayland-*.target

%changelog
* Thu Jan 29 2026 Basil Crow <me@basilcrow.com> - 0.26.1-1
- Initial packaging
