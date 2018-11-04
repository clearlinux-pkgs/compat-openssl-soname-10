Name:           compat-openssl-soname-10
Version:        1.0.2p
Release:        74
License:        OpenSSL
Summary:        Secure Socket Layer
Url:            http://www.openssl.org/
Group:          libs/network
Source0:        http://www.openssl.org/source/openssl-1.0.2p.tar.gz
BuildRequires:  zlib-dev
BuildRequires:  zlib-dev32
BuildRequires:  util-linux-extras
BuildRequires:  util-linux-bin
BuildRequires:  gcc-dev32
BuildRequires:  gcc-libgcc32
BuildRequires:  gcc-libstdc++32
BuildRequires:  glibc-dev32
BuildRequires:  glibc-libc32

Requires:       ca-certs
Requires:       p11-kit

Patch1: 0001-Add-Clear-Linux-standard-CFLAGS.patch
Patch2: 0002-Remove-warning-in-non-fatal-absence-of-etc-ssl-opens.patch
Patch3: 0003-Make-openssl-stateless-configuration.patch
Patch4: 0004-Hide-a-symbol-from-Steam.patch
Patch5: cve-2016-2178.patch

%description
Secure Socket Layer.

%package lib
License:        OpenSSL
Summary:        Secure Socket Layer
Group:          libs/network
Requires:       p11-kit

%description lib
Secure Socket Layer.

%package lib32
License:        OpenSSL
Summary:        Secure Socket Layer
Group:          libs/network

%description lib32
Secure Socket Layer.


%prep
%setup -q -n openssl-1.0.2p
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
pushd ..
cp -a openssl-1.0.2p build32
popd


%build
export AR=gcc-ar
export RANLIB=gcc-ranlib

./config shared no-ssl zlib-dynamic no-rc4 no-ssl2 no-ssl3 \
 --prefix=%{_prefix} \
 --openssldir=/etc/ssl \
 --openssldir_defaults=/usr/share/defaults/ssl \
 --libdir=lib64

# parallel build is broken
make depend
make

pushd ../build32
export CFLAGS="$CFLAGS -m32 -fno-lto" 
export LDFLAGS="$LDFLAGS -m32 -fno-lto" 
export CXXFLAGS="$CXXFLAGS -m32 -fno-lto" 
i386 ./config shared no-ssl zlib-dynamic no-rc4 no-ssl2 no-ssl3 no-asm \
 --prefix=%{_prefix} \
 --openssldir=/etc/ssl \
 --openssldir_defaults=/usr/share/defaults/ssl \
 --libdir=lib32 
make depend
make
popd


%install
pushd ../build32
export CFLAGS="$CFLAGS -m32 -fno-lto" 
export LDFLAGS="$LDFLAGS -m32 -fno-lto" 
export CXXFLAGS="$CXXFLAGS -m32 -fno-lto" 
make  INSTALL_PREFIX=%{buildroot} MANDIR=/usr/share/man MANSUFFIX=openssl install
pushd %{buildroot}/usr/lib32/pkgconfig
for i in *.pc ; do mv $i 32$i ; done
popd
popd

export CFLAGS="$CFLAGS -m64 -flto" 
export LDFLAGS="$LDFLAGS -m64 -flto" 
export CXXFLAGS="$CXXFLAGS -m64 -flto" 

make  INSTALL_PREFIX=%{buildroot} MANDIR=/usr/share/man MANSUFFIX=openssl install

mv %{buildroot}/etc/ssl/misc/c_hash %{buildroot}/usr/bin/c_hash
mv %{buildroot}/etc/ssl/openssl.cnf %{buildroot}/usr/share/defaults/ssl/openssl.cnf
rm -rf %{buildroot}/etc/ssl
rm -rf %{buildroot}/usr/lib64/*.a



%check
make test


%files
%exclude /usr/bin/openssl
%exclude /usr/bin/c_hash
%exclude /usr/share/defaults/ssl/openssl.cnf
%exclude /usr/include/openssl/*.h
%exclude /usr/lib64/libcrypto.so
%exclude /usr/lib64/libssl.so
%exclude /usr/lib64/pkgconfig/libcrypto.pc
%exclude /usr/lib64/pkgconfig/libssl.pc
%exclude /usr/lib64/pkgconfig/openssl.pc
%exclude /usr/bin/c_rehash
%exclude /usr/lib32/libcrypto.so
%exclude /usr/lib32/libssl.so
%exclude /usr/lib32/pkgconfig/32libcrypto.pc
%exclude /usr/lib32/pkgconfig/32libssl.pc
%exclude /usr/lib32/pkgconfig/32openssl.pc
%exclude /usr/lib32/libcrypto.a
%exclude /usr/lib32/libssl.a
%exclude /usr/share/man/man1/*
%exclude /usr/share/man/man3/*
%exclude /usr/share/man/man5/*
%exclude /usr/share/man/man7/*

%files lib
/usr/lib64/libcrypto.so.1.0.0
/usr/lib64/libssl.so.1.0.0
/usr/lib64/engines/lib4758cca.so
/usr/lib64/engines/libaep.so
/usr/lib64/engines/libatalla.so
/usr/lib64/engines/libcapi.so
/usr/lib64/engines/libchil.so
/usr/lib64/engines/libcswift.so
/usr/lib64/engines/libgmp.so
/usr/lib64/engines/libgost.so
/usr/lib64/engines/libnuron.so
/usr/lib64/engines/libpadlock.so
/usr/lib64/engines/libsureware.so
/usr/lib64/engines/libubsec.so


%files lib32
/usr/lib32/libcrypto.so.1.0.0
/usr/lib32/libssl.so.1.0.0
/usr/lib32/engines/lib4758cca.so
/usr/lib32/engines/libaep.so
/usr/lib32/engines/libatalla.so
/usr/lib32/engines/libcapi.so
/usr/lib32/engines/libchil.so
/usr/lib32/engines/libcswift.so
/usr/lib32/engines/libgmp.so
/usr/lib32/engines/libgost.so
/usr/lib32/engines/libnuron.so
/usr/lib32/engines/libpadlock.so
/usr/lib32/engines/libsureware.so
/usr/lib32/engines/libubsec.so

