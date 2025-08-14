docker run --name local-postgres \
    --network pg-network
    -e POSTGRES_USER=$POSTGRES_USER
    -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD
    -e POSTGRES_DB=tasklist
    -p 5432:5432
    -d postgres