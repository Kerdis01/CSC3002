####-RUN 'MAKE' TO INSTALL DEPENDENCIES-####

# Step 1: Install Miniconda

if [ ! -d "$HOME/miniconda3" ]; then
    # Download the latest Miniconda3 install script
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O $HOME/miniconda3.sh
    
    # Run the installer
    bash $HOME/miniconda3.sh -b -p $HOME/miniconda3

    # Remove the installer script
    rm $HOME/miniconda3.sh
else
    echo "Miniconda3 is already installed at $HOME/miniconda3"
fi

# Initialize Conda
source $HOME/miniconda3/etc/profile.d/conda.sh
conda init
exec bash