package tools

import (
	"context"
	"fmt"
	"time"

	"go.mongodb.org/mongo-driver/v2/bson"
	"go.mongodb.org/mongo-driver/v2/mongo/options"
)

type WeightEntry struct {
	DateTime  string  `bson:"datetime"`
	WeightLbs float64 `bson:"weight_lbs"`
}

func (w *WeightDB) logWeight(weight float64) error {
	entry := WeightEntry{
		DateTime:  time.Now().Format(time.RFC3339),
		WeightLbs: weight,
	}

	_, err := w.collection.InsertOne(context.Background(), entry)
	return err
}

func (w *WeightDB) getHistory() ([]WeightEntry, error) {
	opts := options.Find().SetSort(bson.D{{Key: "datetime", Value: 1}})

	cursor, err := w.collection.Find(context.Background(), bson.D{}, opts)
	if err != nil {
		return nil, err
	}
	defer cursor.Close(context.Background())

	var results []WeightEntry
	err = cursor.All(context.Background(), &results)
	return results, err
}

func (w *WeightDB) weightChange() (float64, error) {
	history, err := w.getHistory()
	if err != nil {
		return 0, err
	}

	if len(history) < 2 {
		return 0, fmt.Errorf("not enough data to compute change")
	}

	first := history[0].WeightLbs
	last := history[len(history)-1].WeightLbs

	return last - first, nil
}
