PATH="$HOME/bin:$PATH"
LD_LIBRARY_PATH="$HOME/lib:${LD_LIBRARY_PATH}"
export PATH LD_LIBRARY_PATH
gpg2 --version | grep "gpg (GnuPG) $GPG_VERSION" && exit 0

wget https://gnupg.org/ftp/gcrypt/gnupg/gnupg-$GPG_VERSION.tar.bz2
bzcat gnupg-$GPG_VERSION.tar.bz2 | tar xf -
cd gnupg-$GPG_VERSION
make -f build-aux/speedo.mk native INSTALL_PREFIX="$HOME"

gpg2 --version | grep "gpg (GnuPG) $GPG_VERSION"
