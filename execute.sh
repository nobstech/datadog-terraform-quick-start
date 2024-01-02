#! /usr/bin/bash

pushd () {
  command pushd "$@" > /dev/null
}

popd () {
  command popd "$@" > /dev/null
}

pushd /terraform 
/usr/bin/terraform validate &> /dev/null

if [ $? -ne 0 ]; then
    echo "Terraform and Datadog provider not initialized, initializing..."
    /usr/bin/terraform init
fi
popd

/usr/local/bin/python code/configure.py

find /terraform/datadog -type f -exec sed -i -e 's/tfer--//g' {} \;

/usr/local/bin/python code/migrate.py

pushd /terraform
for d in $(ls datadog)
do
  pushd /terraform/datadog/$d
  /usr/bin/terraform state replace-provider -auto-approve "registry.terraform.io/-/datadog" "DataDog/datadog"
  popd
done
popd

for f in $(find /terraform/datadog -name 'terraform.tfstate.*.backup'); do rm $f; done