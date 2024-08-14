machine_type=$(uname -s)

if [ "$machine_type" = "Darwin" ]
then
    export $(grep -v '^#' .env | tr '\n' '\0' | xargs -0)
else
    export $(grep -v '^#' .env | xargs -d '\n')
fi


while getopts r: flag
do
    case "${flag}" in
        r) repository=${OPTARG};;
    esac
done

if [ "$repository" = "test" ]
then
    poetry publish --repository testpypi -u $TEST_PYPI_TOKEN_USERNAME -p $TEST_PYPI_TOKEN_PASSWORD
else
    poetry publish --repository pypi -u $PYPI_TOKEN_USERNAME -p $PYPI_TOKEN_PASSWORD
fi
