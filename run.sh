#!/bin/bash

set -e

cleanup() {
    echo "Cleaning up Docker containers and images..."
    
    docker ps -aq | xargs -r docker rm -f
    docker images -q | xargs -r docker rmi -f

    echo "Cleanup complete."
    exit 0
}

setup_openssl() {
    echo "Checking for OpenSSL..."

    install_openssl_mac() {
        echo "Checking for Homebrew..."
        if ! command -v brew >/dev/null 2>&1; then
            echo "Homebrew is not installed. Installing Homebrew..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        fi

        echo "Installing OpenSSL via Homebrew..."
        brew install openssl

        echo "Adding OpenSSL to PATH..."
        echo 'export PATH="/usr/local/opt/openssl/bin:$PATH"' >> ~/.bash_profile
        echo 'export PATH="/usr/local/opt/openssl/bin:$PATH"' >> ~/.zshrc
        export PATH="/usr/local/opt/openssl/bin:$PATH"
        echo "OpenSSL installation complete!"
    }

    validate_openssl() {
        if ! command -v openssl >/dev/null 2>&1; then
            echo "OpenSSL is not installed or not in PATH."
            return 1
        fi

        echo "OpenSSL version: $(openssl version)"
        return 0
    }

    generate_ssl_certificate() {
        echo "Generating a self-signed SSL certificate..."
        
        OS="$(uname -s)"
        if [[ "$OS" =~ MINGW*|CYGWIN*|MSYS* ]]; then
            SUBJ="//C=CA\ST=ON\L=London\O=Capstone\OU=Homey\CN=localhost"
        else
            SUBJ="/C=CA/ST=ON/L=London/O=Capstone/OU=Homey/CN=localhost"
        fi

        "$(which openssl)" req -x509 -newkey rsa:4096 \
            -keyout "./backend/key.pem" \
            -out "./backend/cert.crt" \
            -sha256 -days 365 -nodes \
            -subj "$SUBJ"
    }

    OS="$(uname -s)"
    case "$OS" in
        Darwin)
            echo "Running on macOS"
            validate_openssl || install_openssl_mac
            ;;
        MINGW*|CYGWIN*|MSYS*)
            echo "Running on Windows (Git Bash)."

            OPENSSL_PATH=$(which openssl)
            if [[ -z "$OPENSSL_PATH" || "$OPENSSL_PATH" != "/mingw64/bin/openssl" ]]; then
                echo "OpenSSL not found or not in the expected path"
                exit 1
            fi

            echo "OpenSSL binary found at: $OPENSSL_PATH"
            echo "OpenSSL version: $(openssl version)"
            ;;
        *)
            echo "Unsupported operating system: $OS"
            exit 1
            ;;
    esac

    echo "OpenSSL setup completed successfully!"
    if [[ ! -f "./backend/cert.crt" || ! -f "./backend/key.pem" ]]; then
        echo "Certificate or key file not found. Generating SSL certificate..."
        generate_ssl_certificate
    else
        echo "SSL certificate already exists."
    fi
}

trap cleanup SIGINT SIGTERM EXIT

start_frontend() {
    echo "Starting frontend ..."
    (
        cd ./frontend || exit
        npm install
        npx expo install expo@latest
        npx expo install --fix
        npx expo start &
    )
    sleep 15
}

start_backend() {
    echo "Starting backend ..."
    if [[ "$(uname)" != "Darwin" ]]; then
        dos2unix ./backend/docker/scripts/wait-for-db.sh
    fi
    docker compose -f ./backend/docker/docker-compose.yml up --build
}

setup_openssl
start_frontend
start_backend

docker logs -f $(docker ps -q) 