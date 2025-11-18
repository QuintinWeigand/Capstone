package tools

import (
	"context"
	"fmt"

	"go.mongodb.org/mongo-driver/v2/mongo"
	"go.mongodb.org/mongo-driver/v2/mongo/options"
)

type WeightDB struct {
	collection *mongo.Collection
}

func NewWeightDB(collection *mongo.Collection) *WeightDB {
	return &WeightDB{collection: collection}
}

func GetMongoCollection() (*mongo.Collection, error) {
	client, err := mongo.Connect(options.Client().ApplyURI("mongodb://localhost:27017"))
	if err != nil {
		return nil, fmt.Errorf("could not connect to MongoDB: %v", err)
	}

	err = client.Ping(context.Background(), nil)
	if err != nil {
		return nil, fmt.Errorf("Failed to ping MongoDB: %v", err)
	}

	db := client.Database("weight_tracker")
	collection := db.Collection("weights")

	return collection, nil
}
